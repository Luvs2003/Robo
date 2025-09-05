import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf

class AIRebalancer:
    def __init__(self):
        self.rebalancing_threshold = 5.0  # 5% deviation threshold
        self.market_indicators = {
            'volatility_threshold': 20.0,
            'momentum_threshold': 0.05,
            'correlation_threshold': 0.7
        }
        
        self.market_conditions = {
            'bull_market': {'equity_boost': 5, 'debt_reduce': 5},
            'bear_market': {'equity_reduce': 10, 'debt_boost': 10},
            'volatile_market': {'equity_reduce': 5, 'gold_boost': 5},
            'stable_market': {'maintain': True}
        }
    
    def get_rebalancing_recommendations(self, portfolio):
        """Generate AI-powered rebalancing recommendations"""
        recommendations = []
        
        # Analyze current market conditions
        market_condition = self._analyze_market_conditions()
        
        # Check allocation drift
        drift_analysis = self._analyze_allocation_drift(portfolio)
        
        # Generate recommendations based on drift and market conditions
        for asset_class, drift_info in drift_analysis.items():
            if abs(drift_info['drift_percentage']) > self.rebalancing_threshold:
                recommendation = self._generate_recommendation(
                    asset_class, drift_info, market_condition, portfolio
                )
                recommendations.append(recommendation)
        
        # Add market-based recommendations
        market_recommendations = self._get_market_based_recommendations(
            portfolio, market_condition
        )
        recommendations.extend(market_recommendations)
        
        return recommendations
    
    def _analyze_market_conditions(self):
        """Analyze current market conditions using various indicators"""
        # Mock market analysis - in real implementation, this would fetch live data
        market_data = {
            'volatility': np.random.uniform(10, 30),
            'momentum': np.random.uniform(-0.1, 0.1),
            'trend': np.random.choice(['bullish', 'bearish', 'sideways']),
            'correlation': np.random.uniform(0.3, 0.8)
        }
        
        # Determine market condition
        if market_data['volatility'] > 25:
            condition = 'volatile_market'
        elif market_data['momentum'] > 0.03 and market_data['trend'] == 'bullish':
            condition = 'bull_market'
        elif market_data['momentum'] < -0.03 and market_data['trend'] == 'bearish':
            condition = 'bear_market'
        else:
            condition = 'stable_market'
        
        return {
            'condition': condition,
            'data': market_data,
            'confidence': np.random.uniform(0.7, 0.95)
        }
    
    def _analyze_allocation_drift(self, portfolio):
        """Analyze how much the current allocation has drifted from target"""
        target_allocation = portfolio['allocation']
        
        # Mock current allocation (in real implementation, this would be calculated from current market values)
        current_allocation = {}
        drift_analysis = {}
        
        for asset_class, target_pct in target_allocation.items():
            # Simulate some drift
            drift = np.random.uniform(-8, 8)
            current_pct = max(0, target_pct + drift)
            
            current_allocation[asset_class] = current_pct
            drift_analysis[asset_class] = {
                'target_percentage': target_pct,
                'current_percentage': current_pct,
                'drift_percentage': current_pct - target_pct,
                'drift_amount': (current_pct - target_pct) / 100 * portfolio['current_value']
            }
        
        return drift_analysis
    
    def _generate_recommendation(self, asset_class, drift_info, market_condition, portfolio):
        """Generate specific recommendation for an asset class"""
        drift_pct = drift_info['drift_percentage']
        drift_amount = abs(drift_info['drift_amount'])
        
        if drift_pct > self.rebalancing_threshold:
            action = 'SELL'
            reason = f"Overweight by {drift_pct:.1f}% due to market appreciation"
        elif drift_pct < -self.rebalancing_threshold:
            action = 'BUY'
            reason = f"Underweight by {abs(drift_pct):.1f}% due to market decline"
        else:
            action = 'HOLD'
            reason = "Within acceptable allocation range"
        
        # Adjust based on market conditions
        if market_condition['condition'] != 'stable_market':
            reason += f" | Market condition: {market_condition['condition']}"
        
        return {
            'asset': asset_class,
            'action': action,
            'quantity': f"₹{drift_amount:,.0f}",
            'percentage': f"{abs(drift_pct):.1f}%",
            'reason': reason,
            'priority': 'High' if abs(drift_pct) > 10 else 'Medium',
            'market_factor': market_condition['condition']
        }
    
    def _get_market_based_recommendations(self, portfolio, market_condition):
        """Get recommendations based on market conditions"""
        recommendations = []
        condition = market_condition['condition']
        confidence = market_condition['confidence']
        
        if condition == 'bull_market' and confidence > 0.8:
            recommendations.append({
                'asset': 'Equity Allocation',
                'action': 'INCREASE',
                'quantity': '5%',
                'percentage': '5%',
                'reason': f'Bull market detected with {confidence:.1%} confidence - consider increasing equity exposure',
                'priority': 'Medium',
                'market_factor': condition
            })
        
        elif condition == 'bear_market' and confidence > 0.8:
            recommendations.append({
                'asset': 'Debt Allocation',
                'action': 'INCREASE',
                'quantity': '10%',
                'percentage': '10%',
                'reason': f'Bear market detected with {confidence:.1%} confidence - consider defensive positioning',
                'priority': 'High',
                'market_factor': condition
            })
        
        elif condition == 'volatile_market':
            recommendations.append({
                'asset': 'Gold ETF',
                'action': 'INCREASE',
                'quantity': '3%',
                'percentage': '3%',
                'reason': f'High volatility detected - consider increasing gold allocation for stability',
                'priority': 'Medium',
                'market_factor': condition
            })
        
        return recommendations
    
    def calculate_optimal_allocation(self, portfolio, risk_tolerance, market_outlook):
        """Calculate optimal allocation using AI/ML techniques"""
        # Mock implementation of modern portfolio theory with AI enhancements
        base_allocation = portfolio['allocation'].copy()
        
        # Risk adjustment factor
        risk_factors = {
            'Low': 0.8,
            'Medium': 1.0,
            'High': 1.2
        }
        
        risk_factor = risk_factors.get(risk_tolerance, 1.0)
        
        # Market outlook adjustment
        outlook_adjustments = {
            'bullish': {'equity': 5, 'debt': -3, 'gold': -2},
            'bearish': {'equity': -8, 'debt': 5, 'gold': 3},
            'neutral': {'equity': 0, 'debt': 0, 'gold': 0}
        }
        
        adjustments = outlook_adjustments.get(market_outlook, outlook_adjustments['neutral'])
        
        # Apply adjustments
        optimal_allocation = {}
        for asset_class, base_pct in base_allocation.items():
            if 'Equity' in asset_class:
                adjustment = adjustments['equity'] * risk_factor
            elif 'Debt' in asset_class:
                adjustment = adjustments['debt']
            elif 'Gold' in asset_class:
                adjustment = adjustments['gold']
            else:
                adjustment = 0
            
            optimal_allocation[asset_class] = max(0, min(100, base_pct + adjustment))
        
        # Normalize to 100%
        total = sum(optimal_allocation.values())
        if total != 100:
            for asset_class in optimal_allocation:
                optimal_allocation[asset_class] = optimal_allocation[asset_class] / total * 100
        
        return optimal_allocation
    
    def get_rebalancing_schedule(self, portfolio, frequency='quarterly'):
        """Generate automatic rebalancing schedule"""
        schedule = []
        start_date = datetime.now()
        
        frequency_days = {
            'monthly': 30,
            'quarterly': 90,
            'semi-annual': 180,
            'annual': 365
        }
        
        days = frequency_days.get(frequency, 90)
        
        for i in range(4):  # Next 4 rebalancing dates
            rebalance_date = start_date + timedelta(days=days * (i + 1))
            schedule.append({
                'date': rebalance_date.strftime('%Y-%m-%d'),
                'type': 'Scheduled Rebalancing',
                'frequency': frequency.title(),
                'estimated_trades': np.random.randint(2, 6),
                'estimated_cost': f"₹{np.random.randint(500, 2000):,}"
            })
        
        return schedule
    
    def simulate_rebalancing_impact(self, portfolio, proposed_allocation):
        """Simulate the impact of proposed rebalancing"""
        current_allocation = portfolio['allocation']
        portfolio_value = portfolio['current_value']
        
        # Calculate transaction costs (mock)
        total_change = sum(abs(proposed_allocation[asset] - current_allocation.get(asset, 0)) 
                          for asset in proposed_allocation)
        
        transaction_cost = total_change / 100 * portfolio_value * 0.001  # 0.1% transaction cost
        
        # Estimate impact on returns and risk
        current_return = portfolio['expected_return']
        current_risk = portfolio['portfolio_risk']
        
        # Mock calculation of new metrics
        new_return = current_return + np.random.uniform(-0.5, 1.0)
        new_risk = current_risk + np.random.uniform(-1.0, 0.5)
        new_sharpe = new_return / new_risk if new_risk > 0 else 0
        
        return {
            'transaction_cost': transaction_cost,
            'current_return': current_return,
            'new_return': new_return,
            'return_impact': new_return - current_return,
            'current_risk': current_risk,
            'new_risk': new_risk,
            'risk_impact': new_risk - current_risk,
            'current_sharpe': portfolio['sharpe_ratio'],
            'new_sharpe': new_sharpe,
            'sharpe_impact': new_sharpe - portfolio['sharpe_ratio']
        }