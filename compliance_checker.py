from datetime import datetime, timedelta
import pandas as pd

class ComplianceChecker:
    def __init__(self):
        self.sebi_regulations = {
            'investment_advisor_registration': True,
            'client_agreement_executed': True,
            'risk_profiling_completed': True,
            'disclosure_document_provided': True,
            'fee_structure_disclosed': True,
            'conflict_of_interest_declared': True
        }
        
        self.compliance_rules = {
            'max_single_stock_exposure': 10,  # Maximum 10% in single stock
            'max_sector_exposure': 25,        # Maximum 25% in single sector
            'min_diversification': 5,         # Minimum 5 different assets
            'max_small_cap_exposure': 15,     # Maximum 15% in small cap
            'min_liquid_assets': 10,          # Minimum 10% in liquid assets
            'max_international_exposure': 10  # Maximum 10% in international assets
        }
    
    def check_compliance(self):
        """Check overall compliance status"""
        compliance_status = []
        
        # SEBI Registration Compliance
        compliance_status.append({
            'rule': 'SEBI Registration',
            'status': 'PASS' if self.sebi_regulations['investment_advisor_registration'] else 'FAIL',
            'description': 'Investment Advisor registered with SEBI'
        })
        
        # Client Agreement Compliance
        compliance_status.append({
            'rule': 'Client Agreement',
            'status': 'PASS' if self.sebi_regulations['client_agreement_executed'] else 'FAIL',
            'description': 'Client agreement executed and documented'
        })
        
        # Risk Profiling Compliance
        compliance_status.append({
            'rule': 'Risk Profiling',
            'status': 'PASS' if self.sebi_regulations['risk_profiling_completed'] else 'FAIL',
            'description': 'Client risk profiling completed as per SEBI guidelines'
        })
        
        # Disclosure Compliance
        compliance_status.append({
            'rule': 'Disclosure Document',
            'status': 'PASS' if self.sebi_regulations['disclosure_document_provided'] else 'FAIL',
            'description': 'Disclosure document provided to client'
        })
        
        # Fee Structure Compliance
        compliance_status.append({
            'rule': 'Fee Transparency',
            'status': 'PASS' if self.sebi_regulations['fee_structure_disclosed'] else 'FAIL',
            'description': 'Fee structure transparent and disclosed'
        })
        
        # Conflict of Interest Compliance
        compliance_status.append({
            'rule': 'Conflict of Interest',
            'status': 'PASS' if self.sebi_regulations['conflict_of_interest_declared'] else 'FAIL',
            'description': 'Conflicts of interest declared and managed'
        })
        
        return compliance_status
    
    def check_portfolio_compliance(self, portfolio):
        """Check portfolio-specific compliance"""
        compliance_issues = []
        
        holdings_df = pd.DataFrame(portfolio['holdings'])
        
        # Check single asset exposure
        max_exposure = holdings_df['Allocation %'].max()
        if max_exposure > self.compliance_rules['max_single_stock_exposure']:
            compliance_issues.append({
                'rule': 'Single Asset Exposure',
                'status': 'VIOLATION',
                'current_value': f"{max_exposure}%",
                'limit': f"{self.compliance_rules['max_single_stock_exposure']}%",
                'description': f"Single asset exposure exceeds {self.compliance_rules['max_single_stock_exposure']}%"
            })
        
        # Check diversification
        asset_count = len(holdings_df)
        if asset_count < self.compliance_rules['min_diversification']:
            compliance_issues.append({
                'rule': 'Minimum Diversification',
                'status': 'VIOLATION',
                'current_value': asset_count,
                'limit': self.compliance_rules['min_diversification'],
                'description': f"Portfolio has less than {self.compliance_rules['min_diversification']} different assets"
            })
        
        # Check small cap exposure
        small_cap_exposure = holdings_df[holdings_df['Asset Class'] == 'Small Cap Equity']['Allocation %'].sum()
        if small_cap_exposure > self.compliance_rules['max_small_cap_exposure']:
            compliance_issues.append({
                'rule': 'Small Cap Exposure',
                'status': 'WARNING',
                'current_value': f"{small_cap_exposure}%",
                'limit': f"{self.compliance_rules['max_small_cap_exposure']}%",
                'description': f"Small cap exposure exceeds recommended {self.compliance_rules['max_small_cap_exposure']}%"
            })
        
        # Check international exposure
        intl_exposure = holdings_df[holdings_df['Asset Class'] == 'International Funds']['Allocation %'].sum()
        if intl_exposure > self.compliance_rules['max_international_exposure']:
            compliance_issues.append({
                'rule': 'International Exposure',
                'status': 'WARNING',
                'current_value': f"{intl_exposure}%",
                'limit': f"{self.compliance_rules['max_international_exposure']}%",
                'description': f"International exposure exceeds recommended {self.compliance_rules['max_international_exposure']}%"
            })
        
        return compliance_issues
    
    def generate_compliance_report(self, portfolio):
        """Generate comprehensive compliance report"""
        report = {
            'report_date': datetime.now(),
            'portfolio_id': portfolio.get('client_id', 'Unknown'),
            'regulatory_compliance': self.check_compliance(),
            'portfolio_compliance': self.check_portfolio_compliance(portfolio),
            'overall_status': 'COMPLIANT'
        }
        
        # Determine overall status
        violations = [item for item in report['portfolio_compliance'] if item['status'] == 'VIOLATION']
        if violations:
            report['overall_status'] = 'NON-COMPLIANT'
        elif any(item['status'] == 'WARNING' for item in report['portfolio_compliance']):
            report['overall_status'] = 'COMPLIANT WITH WARNINGS'
        
        return report
    
    def get_sebi_guidelines(self):
        """Get relevant SEBI guidelines for investment advisors"""
        guidelines = {
            'registration_requirements': [
                'Minimum net worth of ₹25 lakhs',
                'Professional qualification in finance/economics',
                'Clean track record with no regulatory violations',
                'Adequate infrastructure and systems'
            ],
            'client_obligations': [
                'Execute client agreement before providing advice',
                'Conduct proper risk profiling',
                'Provide disclosure document',
                'Maintain client confidentiality',
                'Act in client\'s best interest'
            ],
            'operational_requirements': [
                'Maintain books of accounts',
                'File periodic returns with SEBI',
                'Comply with code of conduct',
                'Segregate client assets',
                'Maintain audit trail'
            ],
            'fee_structure': [
                'Fee should be transparent and disclosed',
                'No performance-based fees allowed',
                'Maximum fee: 2.5% of assets under advice or ₹1,25,000 per client per year',
                'No brokerage or commission from third parties'
            ]
        }
        
        return guidelines
    
    def validate_client_suitability(self, client_data, portfolio):
        """Validate if portfolio is suitable for client"""
        suitability_checks = []
        
        # Age vs Risk check
        age = client_data.get('age', 30)
        risk_level = client_data.get('risk_appetite', 'Medium')
        
        if age > 55 and risk_level == 'High':
            suitability_checks.append({
                'check': 'Age vs Risk Alignment',
                'status': 'WARNING',
                'message': 'High risk portfolio may not be suitable for clients above 55'
            })
        
        # Investment horizon vs allocation check
        horizon = client_data.get('investment_horizon', 'Medium Term')
        equity_allocation = sum([
            portfolio['allocation'].get('Large Cap Equity', 0),
            portfolio['allocation'].get('Mid Cap Equity', 0),
            portfolio['allocation'].get('Small Cap Equity', 0)
        ])
        
        if horizon.startswith('Short') and equity_allocation > 40:
            suitability_checks.append({
                'check': 'Investment Horizon vs Equity Allocation',
                'status': 'WARNING',
                'message': 'High equity allocation may not be suitable for short-term goals'
            })
        
        # Income vs Investment amount check
        income = client_data.get('income', 500000)
        investment = client_data.get('investment_amount', 100000)
        
        if investment > income * 0.5:
            suitability_checks.append({
                'check': 'Investment Amount vs Income',
                'status': 'WARNING',
                'message': 'Investment amount exceeds 50% of annual income'
            })
        
        return suitability_checks