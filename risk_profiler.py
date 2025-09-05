import numpy as np

class RiskProfiler:
    def __init__(self):
        self.risk_questions = {
            'market_reaction': {
                'Sell immediately': 1,
                'Hold and wait': 3,
                'Buy more': 5
            },
            'experience': {
                'Beginner': 1,
                'Intermediate': 3,
                'Advanced': 5
            },
            'liquidity_need': {
                'Very important': 1,
                'Somewhat important': 3,
                'Not important': 5
            },
            'objective': {
                'Capital preservation': 1,
                'Balanced growth': 3,
                'Aggressive growth': 5
            }
        }
    
    def calculate_risk_score(self, answers):
        """Calculate risk score based on questionnaire answers"""
        total_score = 0
        max_score = 0
        
        # Score market reaction
        total_score += self.risk_questions['market_reaction'][answers['market_reaction']]
        max_score += 5
        
        # Score experience
        total_score += self.risk_questions['experience'][answers['experience']]
        max_score += 5
        
        # Score loss tolerance (direct percentage)
        loss_tolerance_score = min(answers['loss_tolerance'] / 10, 5)  # Cap at 5
        total_score += loss_tolerance_score
        max_score += 5
        
        # Score liquidity need
        total_score += self.risk_questions['liquidity_need'][answers['liquidity_need']]
        max_score += 5
        
        # Score objective
        total_score += self.risk_questions['objective'][answers['objective']]
        max_score += 5
        
        # Additional scoring for extended questionnaire
        if 'volatility_reaction' in answers:
            volatility_scores = {
                'Sell everything immediately': 1,
                'Sell some and keep some': 2,
                'Keep everything': 4,
                'Invest more money': 5
            }
            total_score += volatility_scores.get(answers['volatility_reaction'], 3)
            max_score += 5
        
        if 'time_horizon' in answers:
            horizon_scores = {
                'Less than 1 year': 1,
                '1-3 years': 2,
                '3-5 years': 3,
                '5-10 years': 4,
                'More than 10 years': 5
            }
            total_score += horizon_scores.get(answers['time_horizon'], 3)
            max_score += 5
        
        if 'financial_situation' in answers:
            situation_scores = {
                'Struggling to meet expenses': 1,
                'Meeting expenses with little left': 2,
                'Comfortable with some savings': 4,
                'Very comfortable with substantial savings': 5
            }
            total_score += situation_scores.get(answers['financial_situation'], 3)
            max_score += 5
        
        if 'decision_style' in answers:
            style_scores = {
                'Very conservative, avoid all risks': 1,
                'Somewhat conservative': 2,
                'Balanced approach': 3,
                'Somewhat aggressive': 4,
                'Very aggressive': 5
            }
            total_score += style_scores.get(answers['decision_style'], 3)
            max_score += 5
        
        if 'wealth_percentage' in answers:
            wealth_score = min(answers['wealth_percentage'] / 20, 5)  # Cap at 5
            total_score += wealth_score
            max_score += 5
        
        # Convert to percentage
        risk_score = (total_score / max_score) * 100
        
        # Determine risk category
        if risk_score <= 35:
            category = 'Conservative'
            risk_level = 'Low'
        elif risk_score <= 65:
            category = 'Moderate'
            risk_level = 'Medium'
        else:
            category = 'Aggressive'
            risk_level = 'High'
        
        return {
            'score': round(risk_score, 1),
            'category': category,
            'risk_level': risk_level,
            'recommendations': self._get_recommendations(category)
        }
    
    def _get_recommendations(self, category):
        """Get investment recommendations based on risk category"""
        recommendations = {
            'Conservative': {
                'asset_allocation': {
                    'Equity': '20-30%',
                    'Debt': '60-70%',
                    'Gold': '5-10%',
                    'International': '0-5%'
                },
                'investment_horizon': 'Short to Medium term (1-5 years)',
                'suitable_products': [
                    'Large Cap Mutual Funds',
                    'Hybrid Funds',
                    'Debt Funds',
                    'Fixed Deposits',
                    'Government Securities'
                ],
                'key_focus': 'Capital preservation with modest growth'
            },
            'Moderate': {
                'asset_allocation': {
                    'Equity': '50-60%',
                    'Debt': '30-40%',
                    'Gold': '5-10%',
                    'International': '5-10%'
                },
                'investment_horizon': 'Medium to Long term (3-10 years)',
                'suitable_products': [
                    'Large & Mid Cap Funds',
                    'Balanced Advantage Funds',
                    'ELSS Funds',
                    'Corporate Bond Funds',
                    'Index Funds'
                ],
                'key_focus': 'Balanced growth with moderate risk'
            },
            'Aggressive': {
                'asset_allocation': {
                    'Equity': '70-80%',
                    'Debt': '10-20%',
                    'Gold': '2-5%',
                    'International': '5-10%'
                },
                'investment_horizon': 'Long term (7+ years)',
                'suitable_products': [
                    'Small & Mid Cap Funds',
                    'Sectoral Funds',
                    'International Funds',
                    'Equity ETFs',
                    'Direct Equity'
                ],
                'key_focus': 'Maximum growth potential with higher risk'
            }
        }
        
        return recommendations.get(category, recommendations['Moderate'])
    
    def assess_risk_capacity(self, client_data):
        """Assess client's risk capacity based on financial situation"""
        age = client_data.get('age', 30)
        income = client_data.get('income', 500000)
        investment_amount = client_data.get('investment_amount', 100000)
        
        # Age factor (younger = higher capacity)
        age_score = max(0, (65 - age) / 45 * 100)
        
        # Income factor
        income_score = min(100, (income / 1000000) * 100)
        
        # Investment ratio factor
        investment_ratio = investment_amount / income
        ratio_score = min(100, investment_ratio * 200)
        
        # Overall capacity score
        capacity_score = (age_score * 0.4 + income_score * 0.3 + ratio_score * 0.3)
        
        if capacity_score >= 70:
            capacity_level = 'High'
        elif capacity_score >= 40:
            capacity_level = 'Medium'
        else:
            capacity_level = 'Low'
        
        return {
            'capacity_score': round(capacity_score, 1),
            'capacity_level': capacity_level,
            'age_factor': round(age_score, 1),
            'income_factor': round(income_score, 1),
            'investment_ratio_factor': round(ratio_score, 1)
        }
    
    def get_risk_adjusted_allocation(self, risk_profile, risk_capacity):
        """Get risk-adjusted asset allocation"""
        risk_score = risk_profile['score']
        capacity_score = risk_capacity['capacity_score']
        
        # Adjust risk score based on capacity
        adjusted_score = (risk_score * 0.7 + capacity_score * 0.3)
        
        if adjusted_score <= 35:
            allocation = {
                'Large Cap Equity': 25,
                'Mid Cap Equity': 5,
                'Small Cap Equity': 0,
                'Debt Funds': 60,
                'Gold ETF': 10,
                'International Funds': 0
            }
        elif adjusted_score <= 65:
            allocation = {
                'Large Cap Equity': 40,
                'Mid Cap Equity': 15,
                'Small Cap Equity': 5,
                'Debt Funds': 30,
                'Gold ETF': 5,
                'International Funds': 5
            }
        else:
            allocation = {
                'Large Cap Equity': 50,
                'Mid Cap Equity': 25,
                'Small Cap Equity': 15,
                'Debt Funds': 5,
                'Gold ETF': 3,
                'International Funds': 2
            }
        
        return allocation