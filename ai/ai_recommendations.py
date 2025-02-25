from groq import Groq
from dotenv import load_dotenv

load_dotenv()
import os;

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def get_tax_saving_recommendations(gross_income, deductions):
    """Generate AI-powered tax-saving recommendations using DeepSeek"""
    prompt = f"""
    I have an annual gross income of ₹{gross_income}. My current deductions are:
    - Section 80C: ₹{deductions.get('section_80c', 0)}
    - Health Insurance: ₹{deductions.get('health_insurance', 0)}
    - NPS: ₹{deductions.get('nps', 0)}
    - Housing Loan Interest: ₹{deductions.get('housing_loan', 0)}
    Suggest the best tax-saving options for me under the old and new tax regimes.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful tax assistant."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content 
    except Exception as e:
        return f"Error: {str(e)}"
