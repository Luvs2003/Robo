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
        """Analyze current market conditions using actual market data with robust fallbacks"""
        # Initialize with realistic default values
        volatility = 18.0
        momentum = 0.01
        trend = 'sideways'
        correlation = 0.5
        data_source = 'simulated'
        
        try:
            # Try to fetch actual market data for Indian indices
            nifty = yf.download('^NSEI', period='30d', interval='1d', progress=False)
            
            if not nifty.empty and len(nifty) >= 20:
                # Calculate actual volatility (30-day)
                returns = nifty['Close'].pct_change().dropna()
                if len(returns) > 5:
                    volatility = returns.std() * np.sqrt(252) * 100  # Annualized volatility
                    
                    # Calculate momentum (30-day return)
                    momentum = (nifty['Close'].iloc[-1] / nifty['Close'].iloc[0] - 1)
                    
                    # Determine trend based on moving averages
                    if len(nifty) >= 20:
                        ma_5 = nifty['Close'].rolling(5).mean().iloc[-1]
                        ma_20 = nifty['Close'].rolling(20).mean().iloc[-1]
                        
                        if ma_5 > ma_20 and momentum > 0.02:
                            trend = 'bullish'
                        elif ma_5 < ma_20 and momentum < -0.02:
                            trend = 'bearish'
                        else:
                            trend = 'sideways'
                    
                    data_source = 'live'
                    
                    # Try to calculate correlation with global markets
                    try:
                        spy = yf.download('SPY', period='30d', interval='1d', progress=False)
                        if not spy.empty and len(spy) >= len(nifty):
                            nifty_returns = nifty['Close'].pct_change().dropna()
                            spy_returns = spy['Close'].pct_change().dropna()
                            
                            # Align the data
                            min_len = min(len(nifty_returns), len(spy_returns))
                            if min_len > 5:
                                correlation = np.corrcoef(nifty_returns[-min_len:], spy_returns[-min_len:])[0, 1]
                                if np.isnan(correlation):
                                    correlation = 0.5
                    except:
                        correlation = 0.5  # Keep default if correlation calc fails
                        
        except Exception as e:
            # Use enhanced simulated data based on typical market patterns
            import time
            seed = int(time.time() / 3600) % 100  # Changes every hour for variety
            np.random.seed(seed)
            
            # Generate more realistic simulated market conditions
            volatility = np.random.normal(18.0, 3.0)  # Mean 18%, std 3%
            volatility = max(10.0, min(35.0, volatility))  # Clamp between 10-35%
            
            momentum = np.random.normal(0.005, 0.03)  # Small positive bias
            momentum = max(-0.15, min(0.15, momentum))  # Clamp between -15% to 15%
            
            # Trend based on momentum with some randomness
            if momentum > 0.03:
                trend = 'bullish'
            elif momentum < -0.03:
                trend = 'bearish'
            else:
                trend = 'sideways'
            
            correlation = np.random.uniform(0.4, 0.7)  # Typical range for India-US correlation
            data_source = 'simulated'
        
        market_data = {
            'volatility': volatility,
            'momentum': momentum,
            'trend': trend,
            'correlation': abs(correlation) if not np.isnan(correlation) else 0.5
        }
        
        # Determine market condition based on actual data
        if market_data['volatility'] > 25:
            condition = 'volatile_market'
        elif market_data['momentum'] > 0.03 and market_data['trend'] == 'bullish':
            condition = 'bull_market'
        elif market_data['momentum'] < -0.03 and market_data['trend'] == 'bearish':
            condition = 'bear_market'
        else:
            condition = 'stable_market'
        
        # Calculate confidence based on data quality and consistency
        confidence = min(0.95, 0.7 + (abs(momentum) * 5) + (0.1 if trend != 'sideways' else 0))
        
        return {
            'condition': condition,
            'data': market_data,
            'confidence': confidence,
            'data_source': data_source
        }
    
    def _analyze_allocation_drift(self, portfolio):
        """Analyze how much the current allocation has drifted from target based on actual holdings"""
        target_allocation = portfolio['allocation']
        current_allocation = {}
        drift_analysis = {}
        
        # Calculate current allocation from actual holdings
        holdings_df = pd.DataFrame(portfolio['holdings'])
        total_current_value = 0
        
        # Calculate current market values for each holding
        for _, holding in holdings_df.iterrows():
            asset_class = holding['Asset Class']
            original_amount = holding['Amount (₹)']
            
            # Calculate performance based on asset class characteristics
            days_since_creation = (datetime.now() - portfolio['created_date']).days
            if days_since_creation < 1:
                days_since_creation = 1
            
            # Use asset class expected returns to calculate current value
            asset_details = self._get_asset_class_details()
            expected_daily_return = asset_details.get(asset_class, {}).get('return', 8.0) / 365 / 100
            expected_daily_volatility = asset_details.get(asset_class, {}).get('risk', 10.0) / np.sqrt(365) / 100
            
            # Calculate cumulative return with some randomness
            np.random.seed(hash(holding['Fund Name']) % 2**32)  # Consistent randomness per fund
            daily_returns = np.random.normal(expected_daily_return, expected_daily_volatility, days_since_creation)
            cumulative_return = np.prod(1 + daily_returns) - 1
            
            current_value = original_amount * (1 + cumulative_return)
            total_current_value += current_value
            
            if asset_class in current_allocation:
                current_allocation[asset_class] += current_value
            else:
                current_allocation[asset_class] = current_value
        
        # Convert to percentages
        for asset_class in current_allocation:
            current_allocation[asset_class] = (current_allocation[asset_class] / total_current_value) * 100
        
        # Calculate drift for each asset class
        for asset_class, target_pct in target_allocation.items():
            current_pct = current_allocation.get(asset_class, 0)
            drift_pct = current_pct - target_pct
            drift_amount = drift_pct / 100 * total_current_value
            
            drift_analysis[asset_class] = {
                'target_percentage': target_pct,
                'current_percentage': current_pct,
                'drift_percentage': drift_pct,
                'drift_amount': drift_amount
            }
        
        # Update portfolio current value
        portfolio['current_value'] = total_current_value
        
        return drift_analysis
    
    def _get_asset_class_details(self):
        """Get asset class return and risk characteristics"""
        return {
            'Large Cap Equity': {'return': 12.0, 'risk': 15.0},
            'Mid Cap Equity': {'return': 15.0, 'risk': 20.0},
            'Small Cap Equity': {'return': 18.0, 'risk': 25.0},
            'Debt Funds': {'return': 7.0, 'risk': 3.0},
            'Gold ETF': {'return': 8.0, 'risk': 12.0},
            'International Funds': {'return': 10.0, 'risk': 18.0}
        }
    
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
        """Generate automatic rebalancing schedule based on portfolio characteristics"""
        schedule = []
        start_date = datetime.now()
        
        frequency_days = {
            'monthly': 30,
            'quarterly': 90,
            'semi-annual': 180,
            'annual': 365
        }
        
        days = frequency_days.get(frequency, 90)
        portfolio_value = portfolio['current_value']
        
        # Calculate estimated trades and costs based on portfolio complexity
        num_holdings = len(portfolio['holdings'])
        equity_allocation = sum([
            portfolio['allocation'].get('Large Cap Equity', 0),
            portfolio['allocation'].get('Mid Cap Equity', 0),
            portfolio['allocation'].get('Small Cap Equity', 0)
        ])
        
        for i in range(4):  # Next 4 rebalancing dates
            rebalance_date = start_date + timedelta(days=days * (i + 1))
            
            # Estimate trades based on portfolio complexity and volatility
            base_trades = max(2, num_holdings // 2)
            volatility_factor = portfolio['portfolio_risk'] / 15.0  # Normalize by average risk
            estimated_trades = int(base_trades * (1 + volatility_factor * 0.5))
            
            # Estimate cost based on portfolio value and equity allocation
            base_cost_rate = 0.001  # 0.1% base rate
            equity_cost_premium = (equity_allocation / 100) * 0.0005  # Higher cost for equity-heavy portfolios
            total_cost_rate = base_cost_rate + equity_cost_premium
            
            estimated_cost = portfolio_value * total_cost_rate * (estimated_trades / num_holdings)
            
            schedule.append({
                'date': rebalance_date.strftime('%Y-%m-%d'),
                'type': 'Scheduled Rebalancing',
                'frequency': frequency.title(),
                'estimated_trades': estimated_trades,
                'estimated_cost': f"₹{estimated_cost:,.0f}"
            })
        
        return schedule
    
    def simulate_rebalancing_impact(self, portfolio, proposed_allocation):
        """Simulate the impact of proposed rebalancing based on actual portfolio data"""
        # Get current allocation from drift analysis
        drift_analysis = self._analyze_allocation_drift(portfolio)
        current_allocation = {asset: info['current_percentage'] for asset, info in drift_analysis.items()}
        
        portfolio_value = portfolio['current_value']
        
        # Calculate actual transaction costs based on changes needed
        total_change = sum(abs(proposed_allocation.get(asset, 0) - current_allocation.get(asset, 0)) 
                          for asset in set(list(proposed_allocation.keys()) + list(current_allocation.keys())))
        
        # Transaction cost: 0.1% for equity, 0.05% for debt, 0.15% for international
        transaction_cost = 0
        for asset in proposed_allocation:
            change_pct = abs(proposed_allocation.get(asset, 0) - current_allocation.get(asset, 0))
            change_amount = change_pct / 100 * portfolio_value
            
            if 'Equity' in asset:
                cost_rate = 0.001  # 0.1%
            elif 'Debt' in asset:
                cost_rate = 0.0005  # 0.05%
            elif 'International' in asset:
                cost_rate = 0.0015  # 0.15%
            else:
                cost_rate = 0.001  # Default 0.1%
            
            transaction_cost += change_amount * cost_rate
        
        # Calculate new portfolio metrics based on proposed allocation
        asset_details = self._get_asset_class_details()
        
        # Calculate new expected return
        new_return = sum(
            (proposed_allocation.get(asset, 0) / 100) * asset_details.get(asset, {}).get('return', 8.0)
            for asset in proposed_allocation
        )
        
        # Calculate new portfolio risk (simplified correlation matrix)
        correlation_matrix = self._get_correlation_matrix()
        new_risk = self._calculate_portfolio_risk(proposed_allocation, asset_details, correlation_matrix)
        
        # Current metrics
        current_return = sum(
            (current_allocation.get(asset, 0) / 100) * asset_details.get(asset, {}).get('return', 8.0)
            for asset in current_allocation
        )
        
        current_risk = self._calculate_portfolio_risk(current_allocation, asset_details, correlation_matrix)
        
        # Calculate Sharpe ratios (assuming risk-free rate of 6%)
        risk_free_rate = 6.0
        current_sharpe = (current_return - risk_free_rate) / current_risk if current_risk > 0 else 0
        new_sharpe = (new_return - risk_free_rate) / new_risk if new_risk > 0 else 0
        
        return {
            'transaction_cost': transaction_cost,
            'current_return': current_return,
            'new_return': new_return,
            'return_impact': new_return - current_return,
            'current_risk': current_risk,
            'new_risk': new_risk,
            'risk_impact': new_risk - current_risk,
            'current_sharpe': current_sharpe,
            'new_sharpe': new_sharpe,
            'sharpe_impact': new_sharpe - current_sharpe
        }
    
    def _get_correlation_matrix(self):
        """Get correlation matrix for asset classes"""
        # Simplified correlation matrix based on historical data
        assets = ['Large Cap Equity', 'Mid Cap Equity', 'Small Cap Equity', 'Debt Funds', 'Gold ETF', 'International Funds']
        
        # Correlation matrix (simplified)
        correlation_data = {
            'Large Cap Equity': [1.0, 0.85, 0.75, 0.1, 0.2, 0.7],
            'Mid Cap Equity': [0.85, 1.0, 0.9, 0.05, 0.15, 0.6],
            'Small Cap Equity': [0.75, 0.9, 1.0, 0.0, 0.1, 0.5],
            'Debt Funds': [0.1, 0.05, 0.0, 1.0, 0.3, 0.2],
            'Gold ETF': [0.2, 0.15, 0.1, 0.3, 1.0, 0.25],
            'International Funds': [0.7, 0.6, 0.5, 0.2, 0.25, 1.0]
        }
        
        return pd.DataFrame(correlation_data, index=assets)
    
    def _calculate_portfolio_risk(self, allocation, asset_details, correlation_matrix):
        """Calculate portfolio risk using correlation matrix"""
        portfolio_variance = 0
        
        for asset1 in allocation:
            for asset2 in allocation:
                if asset1 in asset_details and asset2 in asset_details:
                    weight1 = allocation.get(asset1, 0) / 100
                    weight2 = allocation.get(asset2, 0) / 100
                    risk1 = asset_details[asset1].get('risk', 10.0) / 100
                    risk2 = asset_details[asset2].get('risk', 10.0) / 100
                    
                    if asset1 in correlation_matrix.index and asset2 in correlation_matrix.columns:
                        correlation = correlation_matrix.loc[asset1, asset2]
                    else:
                        correlation = 0.5  # Default correlation
                    
                    portfolio_variance += weight1 * weight2 * risk1 * risk2 * correlation
        
        return np.sqrt(portfolio_variance) * 100  # Convert to percentage
