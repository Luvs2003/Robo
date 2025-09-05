import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf

class PortfolioManager:
    def __init__(self):
        self.asset_classes = {
            'Large Cap Equity': {'return': 12.0, 'risk': 15.0, 'allocation': {'Low': 20, 'Medium': 35, 'High': 50}},
            'Mid Cap Equity': {'return': 15.0, 'risk': 20.0, 'allocation': {'Low': 5, 'Medium': 15, 'High': 25}},
            'Small Cap Equity': {'return': 18.0, 'risk': 25.0, 'allocation': {'Low': 0, 'Medium': 5, 'High': 15}},
            'Debt Funds': {'return': 7.0, 'risk': 3.0, 'allocation': {'Low': 60, 'Medium': 35, 'High': 5}},
            'Gold ETF': {'return': 8.0, 'risk': 12.0, 'allocation': {'Low': 10, 'Medium': 5, 'High': 3}},
            'International Funds': {'return': 10.0, 'risk': 18.0, 'allocation': {'Low': 5, 'Medium': 5, 'High': 2}}
        }
        
        self.sample_funds = {
            'Large Cap Equity': ['HDFC Top 100 Fund', 'ICICI Pru Bluechip Fund', 'SBI Large Cap Fund'],
            'Mid Cap Equity': ['HDFC Mid-Cap Opportunities Fund', 'Axis Midcap Fund', 'Kotak Emerging Equity'],
            'Small Cap Equity': ['SBI Small Cap Fund', 'HDFC Small Cap Fund', 'Axis Small Cap Fund'],
            'Debt Funds': ['HDFC Corporate Bond Fund', 'ICICI Pru Corporate Bond', 'Axis Corporate Debt'],
            'Gold ETF': ['HDFC Gold ETF', 'SBI Gold ETF', 'ICICI Pru Gold ETF'],
            'International Funds': ['Motilal Oswal S&P 500', 'HDFC Global Fund', 'ICICI Pru US Bluechip']
        }
    
    def create_portfolio(self, client_data):
        """Create a portfolio based on client's risk profile and goals"""
        risk_appetite = client_data['risk_appetite']
        investment_amount = client_data['investment_amount']
        
        # Calculate allocation based on risk appetite
        allocation = {}
        for asset_class, details in self.asset_classes.items():
            allocation[asset_class] = details['allocation'][risk_appetite]
        
        # Calculate expected return and risk
        expected_return = sum(
            (allocation[asset] / 100) * details['return'] 
            for asset, details in self.asset_classes.items()
        )
        
        portfolio_risk = np.sqrt(sum(
            ((allocation[asset] / 100) * details['risk']) ** 2 
            for asset, details in self.asset_classes.items()
        ))
        
        # Generate holdings
        holdings = []
        for asset_class, percentage in allocation.items():
            if percentage > 0:
                amount = (percentage / 100) * investment_amount
                fund_name = np.random.choice(self.sample_funds[asset_class])
                holdings.append({
                    'Asset Class': asset_class,
                    'Fund Name': fund_name,
                    'Allocation %': percentage,
                    'Amount (₹)': amount,
                    'Units': round(amount / 100, 2),  # Assuming NAV of 100
                    'Current NAV': 100.0
                })
        
        portfolio = {
            'client_id': client_data['name'],
            'allocation': allocation,
            'holdings': holdings,
            'current_value': investment_amount,
            'expected_return': expected_return,
            'portfolio_risk': portfolio_risk,
            'risk_score': self._calculate_risk_score(risk_appetite),
            'sharpe_ratio': expected_return / portfolio_risk if portfolio_risk > 0 else 0,
            'returns': 0.0,  # Initial returns
            'created_date': datetime.now()
        }
        
        return portfolio
    
    def _calculate_risk_score(self, risk_appetite):
        """Calculate risk score on a scale of 1-10"""
        risk_mapping = {'Low': 3.0, 'Medium': 6.0, 'High': 8.5}
        return risk_mapping.get(risk_appetite, 5.0)
    
    def get_performance_data(self, portfolio):
        """Generate mock performance data for visualization"""
        start_date = portfolio['created_date']
        dates = [start_date + timedelta(days=i) for i in range(30)]
        
        # Generate mock performance with some volatility
        initial_value = portfolio['current_value']
        returns = np.random.normal(0.0008, 0.02, 30)  # Daily returns
        values = [initial_value]
        
        for ret in returns[1:]:
            values.append(values[-1] * (1 + ret))
        
        return {
            'dates': dates,
            'values': values
        }
    
    def calculate_portfolio_metrics(self, portfolio):
        """Calculate various portfolio metrics"""
        holdings_df = pd.DataFrame(portfolio['holdings'])
        
        metrics = {
            'total_value': holdings_df['Amount (₹)'].sum(),
            'asset_count': len(holdings_df),
            'largest_holding': holdings_df['Allocation %'].max(),
            'diversification_ratio': len(holdings_df) / holdings_df['Allocation %'].max() * 10
        }
        
        return metrics
    
    def rebalance_portfolio(self, portfolio, target_allocation):
        """Rebalance portfolio to target allocation"""
        current_value = portfolio['current_value']
        rebalancing_actions = []
        
        for asset_class, target_pct in target_allocation.items():
            current_pct = portfolio['allocation'].get(asset_class, 0)
            difference = target_pct - current_pct
            
            if abs(difference) > 1:  # Only rebalance if difference > 1%
                action = 'BUY' if difference > 0 else 'SELL'
                amount = abs(difference / 100 * current_value)
                
                rebalancing_actions.append({
                    'asset_class': asset_class,
                    'action': action,
                    'amount': amount,
                    'percentage_change': difference
                })
        
        return rebalancing_actions