class TaxCalculator:
    def __init__(self):
        # Indian tax slabs for FY 2023-24 (AY 2024-25) - New Tax Regime
        self.tax_brackets_new = [
            (0, 300000, 0),
            (300001, 600000, 0.05),
            (600001, 900000, 0.10),
            (900001, 1200000, 0.15),
            (1200001, 1500000, 0.20),
            (1500001, float('inf'), 0.30)
        ]
        
        # Old Tax Regime
        self.tax_brackets_old = [
            (0, 250000, 0),
            (250001, 500000, 0.05),
            (500001, 1000000, 0.20),
            (1000001, float('inf'), 0.30)
        ]
        
        # Standard deduction
        self.standard_deduction_new = 50000
        self.standard_deduction_old = 50000
        
        # Health and Education Cess rate
        self.cess_rate = 0.04
        
    def calculate_taxable_income_new(self, gross_income):
        """Calculate taxable income under new tax regime"""
        return max(0, gross_income - self.standard_deduction_new)
        
    def calculate_taxable_income_old(self, gross_income, additional_deductions=0):
        """Calculate taxable income under old tax regime with deductions"""
        return max(0, gross_income - self.standard_deduction_old - additional_deductions)
        
    def calculate_tax_liability(self, taxable_income, is_new_regime=True):
        """Calculate tax liability based on taxable income and chosen regime"""
        tax = 0
        tax_brackets = self.tax_brackets_new if is_new_regime else self.tax_brackets_old
        
        for lower_bound, upper_bound, rate in tax_brackets:
            if taxable_income > lower_bound:
                # Calculate the amount of income that falls within this bracket
                bracket_income = min(taxable_income, upper_bound) - lower_bound
                tax += bracket_income * rate
                
            if taxable_income <= upper_bound:
                break
                
        # Add Health and Education Cess (4%)
        tax += tax * self.cess_rate
        
        return tax
    
    def calculate_effective_tax_rate(self, gross_income, tax):
        """Calculate the effective tax rate"""
        if gross_income == 0:
            return 0
        return (tax / gross_income) * 100
    
    def identify_deductions_old_regime(self, has_house_loan=False, has_elss=False, 
                                     has_health_insurance=False, has_nps=False,
                                     section_80c_amount=0, health_insurance_premium=0,
                                     nps_contribution=0, housing_loan_interest=0,
                                     hra_received=0, hra_rent_paid=0, is_metro=False):
        """Identify potential deductions under old regime"""
        potential_deductions = []
        additional_deductions = 0
        
        # Section 80C deductions (max 1.5 lakh)
        if section_80c_amount > 0:
            sec_80c_deduction = min(section_80c_amount, 150000)
            potential_deductions.append(f"Section 80C Deduction: ₹{sec_80c_deduction:,}")
            additional_deductions += sec_80c_deduction
            
        # ELSS investments
        if has_elss:
            potential_deductions.append("ELSS eligible under Section 80C (included in 80C limit)")
            
        # Health Insurance Premium (Section 80D)
        if has_health_insurance and health_insurance_premium > 0:
            health_deduction = min(health_insurance_premium, 25000)
            potential_deductions.append(f"Health Insurance Premium (Sec 80D): ₹{health_deduction:,}")
            additional_deductions += health_deduction
            
        # NPS Contribution (Section 80CCD(1B)) - Additional 50,000
        if has_nps and nps_contribution > 0:
            nps_deduction = min(nps_contribution, 50000)
            potential_deductions.append(f"NPS Contribution (Sec 80CCD(1B)): ₹{nps_deduction:,}")
            additional_deductions += nps_deduction
            
        # Home Loan Interest (Section 24)
        if has_house_loan and housing_loan_interest > 0:
            house_loan_deduction = min(housing_loan_interest, 200000)
            potential_deductions.append(f"Housing Loan Interest (Sec 24): ₹{house_loan_deduction:,}")
            additional_deductions += house_loan_deduction
        
        # HRA Exemption calculation
        if hra_received > 0 and hra_rent_paid > 0:
            # Basic calculation - actual would be more complex
            hra_exemption = min(
                hra_received,
                hra_rent_paid - (0.1 * (hra_received + additional_deductions)),
                0.5 * hra_received if is_metro else 0.4 * hra_received
            )
            if hra_exemption > 0:
                potential_deductions.append(f"HRA Exemption: ₹{hra_exemption:,}")
                additional_deductions += hra_exemption
            
        return potential_deductions, additional_deductions
    
    def process_tax_return(self, gross_income, regime="both", has_house_loan=False, has_elss=False, 
                         has_health_insurance=False, has_nps=False, section_80c_amount=0,
                         health_insurance_premium=0, nps_contribution=0, housing_loan_interest=0,
                         hra_received=0, hra_rent_paid=0, is_metro=False):
        """Process a complete tax return with both regime options"""
        results = {}
        
        # Calculate for new regime (minimal deductions)
        taxable_income_new = self.calculate_taxable_income_new(gross_income)
        tax_liability_new = self.calculate_tax_liability(taxable_income_new, is_new_regime=True)
        effective_tax_rate_new = self.calculate_effective_tax_rate(gross_income, tax_liability_new)
        
        results["new_regime"] = {
            "regime": "New Tax Regime",
            "gross_income": gross_income,
            "standard_deduction": self.standard_deduction_new,
            "additional_deductions": 0,
            "deductions_list": ["Standard Deduction"],
            "taxable_income": taxable_income_new,
            "tax_liability": tax_liability_new,
            "effective_tax_rate": effective_tax_rate_new
        }
        
        # Calculate for old regime (with deductions)
        deductions_list, additional_deductions = self.identify_deductions_old_regime(
            has_house_loan, has_elss, has_health_insurance, has_nps,
            section_80c_amount, health_insurance_premium, nps_contribution,
            housing_loan_interest, hra_received, hra_rent_paid, is_metro
        )
        
        taxable_income_old = self.calculate_taxable_income_old(gross_income, additional_deductions)
        tax_liability_old = self.calculate_tax_liability(taxable_income_old, is_new_regime=False)
        effective_tax_rate_old = self.calculate_effective_tax_rate(gross_income, tax_liability_old)
        
        deductions_list.insert(0, "Standard Deduction")
        
        results["old_regime"] = {
            "regime": "Old Tax Regime",
            "gross_income": gross_income,
            "standard_deduction": self.standard_deduction_old,
            "additional_deductions": additional_deductions,
            "deductions_list": deductions_list,
            "taxable_income": taxable_income_old,
            "tax_liability": tax_liability_old,
            "effective_tax_rate": effective_tax_rate_old
        }
        
        # Determine which regime is better
        if tax_liability_new < tax_liability_old:
            results["recommended_regime"] = "new_regime"
        else:
            results["recommended_regime"] = "old_regime"
            
        return results