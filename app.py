from flask import Flask, render_template, request, jsonify
from tax_calculator import TaxCalculator
from ai.ai_chatbot import get_ai_response
from ai.ai_recommendations import get_tax_saving_recommendations

app = Flask(__name__)  # Fixed _name_ to __name__
tax_calculator = TaxCalculator()

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Process tax calculation request"""
    try:
        # Extract data from form
        gross_income = float(request.form.get('gross_income', 0))
        
        # Get regime preference
        regime = request.form.get('regime', 'both')
        
        # Get deduction information
        has_house_loan = request.form.get('has_house_loan') == 'yes'
        has_elss = request.form.get('has_elss') == 'yes'
        has_health_insurance = request.form.get('has_health_insurance') == 'yes'
        has_nps = request.form.get('has_nps') == 'yes'
        
        # Get deduction amounts
        section_80c_amount = float(request.form.get('section_80c_amount', 0))
        health_insurance_premium = float(request.form.get('health_insurance_premium', 0))
        nps_contribution = float(request.form.get('nps_contribution', 0))
        housing_loan_interest = float(request.form.get('housing_loan_interest', 0))
        
        # HRA details
        hra_received = float(request.form.get('hra_received', 0))
        hra_rent_paid = float(request.form.get('hra_rent_paid', 0))
        is_metro = request.form.get('is_metro') == 'yes'
        
        # Process tax return
        result = tax_calculator.process_tax_return(
            gross_income, regime, has_house_loan, has_elss, 
            has_health_insurance, has_nps, section_80c_amount,
            health_insurance_premium, nps_contribution, housing_loan_interest,
            hra_received, hra_rent_paid, is_metro
        )
        
        # Add AI-powered insights
        deductions = {
            "section_80c": section_80c_amount,
            "health_insurance": health_insurance_premium,
            "nps": nps_contribution,
            "housing_loan": housing_loan_interest
        }
        result["ai_insights"] = get_tax_saving_recommendations(gross_income, deductions)
        
        # Render result page with tax information
        return render_template('result.html', result=result)
    
    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 400

@app.route('/ask', methods=['POST'])
def ask():
    """Handle AI chatbot queries"""
    user_question = request.form.get('question')
    # Pass tax_calculator instance to get_ai_response
    ai_response = get_ai_response(user_question, tax_calculator)
    return jsonify({"response": ai_response})

if __name__ == '__main__':  # Fixed _name_ and _main_
    app.run(debug=True)