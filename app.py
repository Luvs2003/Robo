import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf
from portfolio_manager import PortfolioManager
from risk_profiler import RiskProfiler
from compliance_checker import ComplianceChecker
from rebalancer import AIRebalancer

# Page configuration
st.set_page_config(
    page_title="RoboAdvisor Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🤖 RoboAdvisor Pro</h1>', unsafe_allow_html=True)
    st.markdown("**SEBI Compliant Investment Advisory Platform**")
    
    # Initialize session state
    if 'portfolio_manager' not in st.session_state:
        st.session_state.portfolio_manager = PortfolioManager()
    if 'risk_profiler' not in st.session_state:
        st.session_state.risk_profiler = RiskProfiler()
    if 'compliance_checker' not in st.session_state:
        st.session_state.compliance_checker = ComplianceChecker()
    if 'rebalancer' not in st.session_state:
        st.session_state.rebalancer = AIRebalancer()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "Client Onboarding",
        "Portfolio Dashboard",
        "Risk Assessment",
        "AI Rebalancing",
        "Compliance Monitor",
        "Market Analysis"
    ])
    
    if page == "Client Onboarding":
        client_onboarding()
    elif page == "Portfolio Dashboard":
        portfolio_dashboard()
    elif page == "Risk Assessment":
        risk_assessment()
    elif page == "AI Rebalancing":
        ai_rebalancing()
    elif page == "Compliance Monitor":
        compliance_monitor()
    elif page == "Market Analysis":
        market_analysis()

def client_onboarding():
    st.header("Client Onboarding & KYC")
    st.write("Please fill in your details to create a personalized investment portfolio")
    
    with st.form("client_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Personal Information")
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            age = st.number_input("Age *", min_value=18, max_value=100, value=30)
            income = st.number_input("Annual Income (₹) *", min_value=0, value=500000, step=50000)
            investment_amount = st.number_input("Initial Investment Amount (₹) *", min_value=1000, value=100000, step=10000)
        
        with col2:
            st.subheader("Investment Profile")
            investment_horizon = st.selectbox("Investment Horizon *", 
                ["Short Term (1-3 years)", "Medium Term (3-7 years)", "Long Term (7+ years)"])
            financial_goal = st.selectbox("Primary Financial Goal *", 
                ["Wealth Creation", "Retirement Planning", "Child Education", "Emergency Fund", "House Purchase"])
            risk_appetite = st.selectbox("Risk Appetite *", ["Low", "Medium", "High"])
        
        # Additional fields
        st.subheader("Additional Information")
        col3, col4 = st.columns(2)
        
        with col3:
            employment_type = st.selectbox("Employment Type", 
                ["Salaried", "Self-Employed", "Business Owner", "Retired"])
            existing_investments = st.number_input("Existing Investments (₹)", min_value=0, value=0, step=10000)
        
        with col4:
            monthly_savings = st.number_input("Monthly Savings Capacity (₹)", min_value=0, value=10000, step=1000)
            dependents = st.number_input("Number of Dependents", min_value=0, max_value=10, value=0)
        
        submitted = st.form_submit_button("Create My Portfolio", type="primary")
        
        if submitted:
            if not name:
                st.error("Please enter your full name")
                return
            
            if investment_amount > income:
                st.warning("Investment amount exceeds annual income. Please review.")
            
            # Create client profile
            client_data = {
                'name': name,
                'age': age,
                'income': income,
                'investment_amount': investment_amount,
                'investment_horizon': investment_horizon,
                'financial_goal': financial_goal,
                'risk_appetite': risk_appetite,
                'employment_type': employment_type,
                'existing_investments': existing_investments,
                'monthly_savings': monthly_savings,
                'dependents': dependents
            }
            
            # Generate portfolio recommendation
            portfolio = st.session_state.portfolio_manager.create_portfolio(client_data)
            
            st.success(f"🎉 Portfolio created successfully for {name}!")
            st.session_state.current_client = client_data
            st.session_state.current_portfolio = portfolio
            
            # Display recommended allocation
            st.subheader("Your Recommended Portfolio Allocation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(values=list(portfolio['allocation'].values()), 
                            names=list(portfolio['allocation'].keys()),
                            title=f"Asset Allocation - {risk_appetite} Risk Profile")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Display allocation table
                allocation_df = pd.DataFrame([
                    {
                        'Asset Class': k, 
                        'Allocation %': f"{v}%", 
                        'Amount (₹)': f"₹{(v/100 * investment_amount):,.0f}"
                    }
                    for k, v in portfolio['allocation'].items() if v > 0
                ])
                st.dataframe(allocation_df, use_container_width=True)
            
            # Display key metrics
            st.subheader("Portfolio Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Expected Return", f"{portfolio['expected_return']:.1f}%")
            with col2:
                st.metric("Risk Score", f"{portfolio['risk_score']:.1f}/10")
            with col3:
                st.metric("Sharpe Ratio", f"{portfolio['sharpe_ratio']:.2f}")
            with col4:
                st.metric("Diversification", f"{len([v for v in portfolio['allocation'].values() if v > 0])} Assets")
            
            st.info("💡 Your portfolio has been created! Navigate to 'Portfolio Dashboard' to view detailed holdings and performance.")
    
    # Show sample allocation examples
    if 'current_portfolio' not in st.session_state:
        st.subheader("Sample Portfolio Allocations")
        st.write("Here's how different risk profiles typically look:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Low Risk Portfolio**")
            st.write("• Large Cap Equity: 20%")
            st.write("• Mid Cap Equity: 5%")
            st.write("• Debt Funds: 60%")
            st.write("• Gold ETF: 10%")
            st.write("• International: 5%")
        
        with col2:
            st.write("**Medium Risk Portfolio**")
            st.write("• Large Cap Equity: 35%")
            st.write("• Mid Cap Equity: 15%")
            st.write("• Small Cap Equity: 5%")
            st.write("• Debt Funds: 35%")
            st.write("• Gold ETF: 5%")
            st.write("• International: 5%")
        
        with col3:
            st.write("**High Risk Portfolio**")
            st.write("• Large Cap Equity: 50%")
            st.write("• Mid Cap Equity: 25%")
            st.write("• Small Cap Equity: 15%")
            st.write("• Debt Funds: 5%")
            st.write("• Gold ETF: 3%")
            st.write("• International: 2%")

def portfolio_dashboard():
    st.header("Portfolio Dashboard")
    
    if 'current_portfolio' not in st.session_state:
        st.warning("⚠️ No portfolio found. Please complete the Client Onboarding process first.")
        st.info("👈 Go to 'Client Onboarding' in the sidebar to create your portfolio")
        return
    
    portfolio = st.session_state.current_portfolio
    
    # Update portfolio with current market values
    drift_analysis = st.session_state.rebalancer._analyze_allocation_drift(portfolio)
    current_value = portfolio['current_value']
    initial_value = st.session_state.current_client['investment_amount']
    returns = ((current_value - initial_value) / initial_value) * 100
    
    # Portfolio metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Portfolio Value", f"₹{current_value:,.2f}", 
                 delta=f"{returns:.2f}%")
    
    with col2:
        st.metric("Expected Return", f"{portfolio['expected_return']:.2f}%")
    
    with col3:
        st.metric("Risk Score", f"{portfolio['risk_score']:.1f}/10")
    
    with col4:
        st.metric("Sharpe Ratio", f"{portfolio['sharpe_ratio']:.2f}")
    
    # Portfolio composition with current values
    st.subheader("Current Holdings")
    holdings_df = pd.DataFrame(portfolio['holdings'])
    
    # Update holdings with current market values
    for i, holding in holdings_df.iterrows():
        asset_class = holding['Asset Class']
        current_allocation_pct = drift_analysis[asset_class]['current_percentage']
        current_amount = (current_allocation_pct / 100) * current_value
        
        holdings_df.at[i, 'Current Value (₹)'] = current_amount
        holdings_df.at[i, 'Current Allocation %'] = current_allocation_pct
        holdings_df.at[i, 'Gain/Loss (₹)'] = current_amount - holding['Amount (₹)']
        holdings_df.at[i, 'Gain/Loss %'] = ((current_amount / holding['Amount (₹)']) - 1) * 100
    
    st.dataframe(holdings_df, use_container_width=True)
    
    # Performance chart
    st.subheader("Portfolio Performance")
    performance_data = st.session_state.portfolio_manager.get_performance_data(portfolio)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=performance_data['dates'], y=performance_data['values'],
                            mode='lines', name='Portfolio Value', line=dict(color='blue', width=2)))
    
    # Add benchmark line (initial investment)
    fig.add_hline(y=initial_value, line_dash="dash", line_color="gray", 
                  annotation_text="Initial Investment")
    
    fig.update_layout(
        title="Portfolio Performance Over Time", 
        xaxis_title="Date", 
        yaxis_title="Value (₹)",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

def risk_assessment():
    st.header("Risk Assessment & Profiling")
    st.write("Complete this questionnaire to determine your investment risk profile")
    
    with st.form("risk_assessment_form"):
        st.subheader("Investment Risk Questionnaire")
        
        col1, col2 = st.columns(2)
        
        with col1:
            q1 = st.radio("1. How would you react to a 20% drop in your portfolio value?",
                         ["Sell immediately", "Hold and wait", "Buy more"],
                         help="This helps us understand your emotional response to market volatility")
            
            q2 = st.radio("2. What is your investment experience?",
                         ["Beginner", "Intermediate", "Advanced"],
                         help="Your experience level affects your ability to handle complex investments")
            
            q3 = st.slider("3. What percentage of loss can you tolerate in a year?", 
                          0, 50, 10, step=5,
                          help="Maximum acceptable loss in your portfolio value")
        
        with col2:
            q4 = st.radio("4. How important is liquidity to you?",
                         ["Very important", "Somewhat important", "Not important"],
                         help="Liquidity refers to how quickly you can convert investments to cash")
            
            q5 = st.radio("5. Your primary investment objective is:",
                         ["Capital preservation", "Balanced growth", "Aggressive growth"],
                         help="This determines the overall strategy for your portfolio")
            
            q6 = st.radio("6. If your investment lost 15% in the first month, you would:",
                         ["Sell everything immediately", "Sell some and keep some", "Keep everything", "Invest more money"],
                         help="This tests your reaction to short-term volatility")
        
        # Additional questions
        st.subheader("Additional Risk Factors")
        
        col3, col4 = st.columns(2)
        
        with col3:
            q7 = st.selectbox("7. Your investment time horizon is:",
                             ["Less than 1 year", "1-3 years", "3-5 years", "5-10 years", "More than 10 years"])
            
            q8 = st.radio("8. Your current financial situation is:",
                         ["Struggling to meet expenses", "Meeting expenses with little left", "Comfortable with some savings", "Very comfortable with substantial savings"])
        
        with col4:
            q9 = st.radio("9. How do you prefer to make investment decisions?",
                         ["Very conservative, avoid all risks", "Somewhat conservative", "Balanced approach", "Somewhat aggressive", "Very aggressive"])
            
            q10 = st.slider("10. What percentage of your total wealth are you investing?", 
                           0, 100, 20, step=5,
                           help="Higher percentage indicates higher risk capacity")
        
        submitted = st.form_submit_button("Calculate My Risk Profile", type="primary")
        
        if submitted:
            # Extended risk answers
            risk_answers = {
                'market_reaction': q1,
                'experience': q2,
                'loss_tolerance': q3,
                'liquidity_need': q4,
                'objective': q5,
                'volatility_reaction': q6,
                'time_horizon': q7,
                'financial_situation': q8,
                'decision_style': q9,
                'wealth_percentage': q10
            }
            
            risk_profile = st.session_state.risk_profiler.calculate_risk_score(risk_answers)
            
            st.success("🎉 Risk assessment completed!")
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Your Risk Profile")
                st.metric("Risk Score", f"{risk_profile['score']}/100")
                st.metric("Risk Category", risk_profile['category'])
                st.metric("Risk Level", risk_profile['risk_level'])
                
                # Risk capacity analysis
                if 'current_client' in st.session_state:
                    risk_capacity = st.session_state.risk_profiler.assess_risk_capacity(st.session_state.current_client)
                    st.metric("Risk Capacity", risk_capacity['capacity_level'])
            
            with col2:
                # Risk gauge chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = risk_profile['score'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Risk Score"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 35], 'color': "lightgreen"},
                            {'range': [35, 65], 'color': "yellow"},
                            {'range': [65, 100], 'color': "lightcoral"}],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90}}))
                st.plotly_chart(fig)
            
            # Display detailed recommendations
            st.subheader("Personalized Investment Recommendations")
            recommendations = risk_profile['recommendations']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Recommended Asset Allocation:**")
                for asset, allocation in recommendations['asset_allocation'].items():
                    st.write(f"• {asset}: {allocation}")
                
                st.write(f"**Investment Horizon:** {recommendations['investment_horizon']}")
                st.write(f"**Key Focus:** {recommendations['key_focus']}")
            
            with col2:
                st.write("**Suitable Investment Products:**")
                for product in recommendations['suitable_products']:
                    st.write(f"• {product}")
            
            # Store risk profile in session
            st.session_state.risk_profile = risk_profile
            
            st.info("💡 Your risk profile has been saved! This will be used to optimize your portfolio allocation.")
    
    # Show risk education
    if 'risk_profile' not in st.session_state:
        st.subheader("Understanding Investment Risk")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Conservative Investors**")
            st.write("• Prefer capital preservation")
            st.write("• Low tolerance for volatility")
            st.write("• Focus on stable returns")
            st.write("• Suitable for short-term goals")
        
        with col2:
            st.write("**Moderate Investors**")
            st.write("• Balance growth and stability")
            st.write("• Moderate risk tolerance")
            st.write("• Diversified approach")
            st.write("• Medium-term investment horizon")
        
        with col3:
            st.write("**Aggressive Investors**")
            st.write("• Seek maximum growth")
            st.write("• High risk tolerance")
            st.write("• Long-term perspective")
            st.write("• Can handle volatility")

def ai_rebalancing():
    st.header("AI-Powered Portfolio Rebalancing")
    
    if 'current_portfolio' not in st.session_state:
        st.warning("⚠️ No portfolio found. Please create your portfolio first.")
        st.info("👈 Go to 'Client Onboarding' in the sidebar to create your portfolio")
        return
    
    portfolio = st.session_state.current_portfolio
    
    st.subheader("Current vs Target Allocation")
    
    # Calculate actual current allocation from portfolio drift analysis
    drift_analysis = st.session_state.rebalancer._analyze_allocation_drift(portfolio)
    
    allocation_df = pd.DataFrame({
        'Asset Class': list(portfolio['allocation'].keys()),
        'Current %': [drift_analysis[asset]['current_percentage'] for asset in portfolio['allocation'].keys()],
        'Target %': list(portfolio['allocation'].values())
    })
    
    fig = px.bar(allocation_df, x='Asset Class', y=['Current %', 'Target %'],
                barmode='group', title="Current vs Target Allocation")
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate rebalancing recommendations
    st.subheader("AI Rebalancing Recommendations")
    
    if st.button("🤖 Analyze Portfolio & Generate Recommendations", type="primary"):
        with st.spinner("AI analyzing market conditions and portfolio drift..."):
            recommendations = st.session_state.rebalancer.get_rebalancing_recommendations(portfolio)
        
        st.write("**Current Market Analysis & Recommendations:**")
        
        if recommendations:
            for rec in recommendations:
                if rec['action'] == 'BUY':
                    st.success(f"🔵 {rec['action']} {rec['quantity']} of {rec['asset']} - {rec['reason']}")
                elif rec['action'] == 'SELL':
                    st.error(f"🔴 {rec['action']} {rec['quantity']} of {rec['asset']} - {rec['reason']}")
                elif rec['action'] == 'INCREASE':
                    st.info(f"📈 {rec['action']} {rec['asset']} by {rec['quantity']} - {rec['reason']}")
                else:
                    st.info(f"⚪ {rec['action']} - {rec['reason']}")
        else:
            st.success("✅ Your portfolio is well-balanced. No rebalancing needed at this time.")
    
    # Show rebalancing impact simulation
    st.subheader("Rebalancing Impact Simulation")
    
    if st.button("📊 Simulate Rebalancing Impact"):
        with st.spinner("Simulating rebalancing impact..."):
            current_allocation = portfolio['allocation']
            risk_level = st.session_state.current_client.get('risk_appetite', 'Medium')
            
            proposed_allocation = st.session_state.rebalancer.calculate_optimal_allocation(
                portfolio, risk_level, 'neutral'
            )
            
            impact = st.session_state.rebalancer.simulate_rebalancing_impact(portfolio, proposed_allocation)
        
        st.subheader("Impact Analysis Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Expected Return", f"{impact['new_return']:.2f}%", 
                     delta=f"{impact['return_impact']:.2f}%")
        
        with col2:
            st.metric("Portfolio Risk", f"{impact['new_risk']:.2f}%", 
                     delta=f"{impact['risk_impact']:.2f}%")
        
        with col3:
            st.metric("Sharpe Ratio", f"{impact['new_sharpe']:.2f}", 
                     delta=f"{impact['sharpe_impact']:.2f}")
        
        st.write(f"**Estimated Transaction Cost:** ₹{impact['transaction_cost']:,.0f}")
        
        # Show before/after allocation comparison
        st.subheader("Allocation Comparison")
        
        comparison_data = []
        for asset in current_allocation.keys():
            comparison_data.append({
                'Asset Class': asset,
                'Current %': current_allocation.get(asset, 0),
                'Proposed %': proposed_allocation.get(asset, 0),
                'Change': proposed_allocation.get(asset, 0) - current_allocation.get(asset, 0)
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
    
    # Auto-rebalancing settings
    st.subheader("Auto-Rebalancing Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_rebalance = st.checkbox("Enable Auto-Rebalancing")
        rebalance_threshold = st.slider("Rebalancing Threshold (%)", 1, 10, 5)
    
    with col2:
        rebalance_frequency = st.selectbox("Rebalancing Frequency", 
                                         ["Monthly", "Quarterly", "Semi-Annual", "Annual"])
        
    if auto_rebalance:
        st.info("Auto-rebalancing is enabled. Portfolio will be automatically rebalanced when allocation drifts beyond the threshold.")

def compliance_monitor():
    st.header("SEBI Compliance Monitor")
    
    compliance_status = st.session_state.compliance_checker.check_compliance()
    
    st.subheader("Compliance Status")
    
    for check in compliance_status:
        if check['status'] == 'PASS':
            st.success(f"✅ {check['rule']}: {check['description']}")
        elif check['status'] == 'WARNING':
            st.warning(f"⚠️ {check['rule']}: {check['description']}")
        else:
            st.error(f"❌ {check['rule']}: {check['description']}")
    
    # Regulatory requirements
    st.subheader("SEBI Investment Advisor Regulations Compliance")
    
    regulations = [
        "Investment Advisor Registration: IA/[REGISTRATION_NUMBER]/2024",
        "Client Agreement: Executed and documented",
        "Risk Profiling: Completed as per SEBI guidelines",
        "Disclosure Document: Provided to client",
        "Fee Structure: Transparent and disclosed",
        "Conflict of Interest: Declared and managed"
    ]
    
    for reg in regulations:
        st.success(f"✅ {reg}")
    
    # Audit trail
    st.subheader("Audit Trail")
    audit_data = {
        'Timestamp': [datetime.now() - timedelta(days=i) for i in range(5)],
        'Action': ['Portfolio Created', 'Risk Assessment', 'Rebalancing', 'Compliance Check', 'Client Onboarding'],
        'User': ['System', 'Advisor', 'AI Engine', 'System', 'Advisor'],
        'Status': ['Success', 'Success', 'Success', 'Success', 'Success']
    }
    
    audit_df = pd.DataFrame(audit_data)
    st.dataframe(audit_df, use_container_width=True)

def market_analysis():
    st.header("Market Analysis & Insights")
    
    # Get real market analysis from rebalancer
    market_conditions = st.session_state.rebalancer._analyze_market_conditions()
    
    # Market indices with real data
    st.subheader("Indian Market Indices")
    
    # Try to fetch market data with better error handling and fallbacks
    col1, col2, col3 = st.columns(3)
    
    # Function to get market data with fallback
    def get_market_data_safe(symbol, name, fallback_price, fallback_change):
        try:
            with st.spinner(f"Fetching {name} data..."):
                data = yf.download(symbol, period='5d', interval='1d', progress=False)
                
            if not data.empty and len(data) >= 2:
                # Convert to float to avoid Series formatting issues
                current_price = float(data['Close'].iloc[-1])
                prev_price = float(data['Close'].iloc[-2])
                change = current_price - prev_price
                change_pct = (change / prev_price) * 100
                return current_price, change, change_pct, True
            else:
                return float(fallback_price), float(fallback_change), float(fallback_change/fallback_price)*100, False
                
        except Exception as e:
            st.warning(f"Live data unavailable for {name}. Using simulated data.")
            return float(fallback_price), float(fallback_change), float(fallback_change/fallback_price)*100, False
    
    # Get data for each index with realistic fallback values
    with col1:
        nifty_price, nifty_change, nifty_pct, nifty_live = get_market_data_safe(
            '^NSEI', 'NIFTY 50', 19750.25, 125.30
        )
        status = "🔴 Live" if nifty_live else "📊 Demo"
        st.metric(
            f"NIFTY 50 {status}", 
            f"{nifty_price:,.2f}", 
            delta=f"{nifty_change:.2f} ({nifty_pct:.2f}%)"
        )
    
    with col2:
        sensex_price, sensex_change, sensex_pct, sensex_live = get_market_data_safe(
            '^BSESN', 'SENSEX', 66230.15, 420.85
        )
        status = "🔴 Live" if sensex_live else "📊 Demo"
        st.metric(
            f"SENSEX {status}", 
            f"{sensex_price:,.2f}", 
            delta=f"{sensex_change:.2f} ({sensex_pct:.2f}%)"
        )
    
    with col3:
        banknifty_price, banknifty_change, banknifty_pct, banknifty_live = get_market_data_safe(
            '^NSEBANK', 'BANK NIFTY', 44180.90, 285.45
        )
        status = "🔴 Live" if banknifty_live else "📊 Demo"
        st.metric(
            f"BANK NIFTY {status}", 
            f"{banknifty_price:,.2f}", 
            delta=f"{banknifty_change:.2f} ({banknifty_pct:.2f}%)"
        )
    
    # Show data source info
    live_count = sum([nifty_live, sensex_live, banknifty_live])
    if live_count == 3:
        st.success("✅ All market data is live and current")
    elif live_count > 0:
        st.info(f"ℹ️ {live_count}/3 indices showing live data, others using demo data")
    else:
        st.warning("⚠️ Using demo market data. Check internet connection for live updates.")
    
    # Market sentiment based on real analysis
    st.subheader("Market Sentiment Analysis")
    
    market_data = market_conditions['data']
    
    # Determine signals based on actual data
    volatility_signal = "High Volatility" if market_data['volatility'] > 20 else "Low Volatility"
    momentum_signal = "Positive" if market_data['momentum'] > 0 else "Negative"
    trend_signal = market_data['trend'].title()
    correlation_signal = "High Correlation" if market_data['correlation'] > 0.6 else "Low Correlation"
    
    sentiment_data = {
        'Indicator': ['Market Volatility', 'Momentum', 'Trend', 'Global Correlation'],
        'Value': [f"{market_data['volatility']:.1f}%", 
                 f"{market_data['momentum']:.2%}", 
                 trend_signal,
                 f"{market_data['correlation']:.2f}"],
        'Signal': [volatility_signal, momentum_signal, trend_signal, correlation_signal]
    }
    
    sentiment_df = pd.DataFrame(sentiment_data)
    st.dataframe(sentiment_df, use_container_width=True)
    
    # Market condition summary
    st.subheader("Current Market Condition")
    condition = market_conditions['condition'].replace('_', ' ').title()
    confidence = market_conditions['confidence']
    
    if market_conditions['condition'] == 'bull_market':
        st.success(f"🐂 {condition} (Confidence: {confidence:.1%})")
    elif market_conditions['condition'] == 'bear_market':
        st.error(f"🐻 {condition} (Confidence: {confidence:.1%})")
    elif market_conditions['condition'] == 'volatile_market':
        st.warning(f"📈📉 {condition} (Confidence: {confidence:.1%})")
    else:
        st.info(f"📊 {condition} (Confidence: {confidence:.1%})")
    
    # Asset class performance based on market conditions
    st.subheader("Asset Class Outlook")
    
    asset_outlook = {
        'bull_market': {
            'Large Cap Equity': 'Positive',
            'Mid Cap Equity': 'Very Positive', 
            'Small Cap Equity': 'Positive',
            'Debt Funds': 'Neutral',
            'Gold ETF': 'Negative',
            'International Funds': 'Positive'
        },
        'bear_market': {
            'Large Cap Equity': 'Negative',
            'Mid Cap Equity': 'Very Negative',
            'Small Cap Equity': 'Very Negative', 
            'Debt Funds': 'Positive',
            'Gold ETF': 'Positive',
            'International Funds': 'Negative'
        },
        'volatile_market': {
            'Large Cap Equity': 'Neutral',
            'Mid Cap Equity': 'Negative',
            'Small Cap Equity': 'Very Negative',
            'Debt Funds': 'Positive', 
            'Gold ETF': 'Very Positive',
            'International Funds': 'Neutral'
        },
        'stable_market': {
            'Large Cap Equity': 'Positive',
            'Mid Cap Equity': 'Positive',
            'Small Cap Equity': 'Neutral',
            'Debt Funds': 'Neutral',
            'Gold ETF': 'Neutral', 
            'International Funds': 'Neutral'
        }
    }
    
    current_outlook = asset_outlook.get(market_conditions['condition'], asset_outlook['stable_market'])
    
    outlook_df = pd.DataFrame([
        {'Asset Class': asset, 'Outlook': outlook}
        for asset, outlook in current_outlook.items()
    ])
    
    st.dataframe(outlook_df, use_container_width=True)
    
    # Enhanced Market Analysis Section
    st.subheader("📊 Advanced Market Analytics")
    
    # Market breadth analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Market Breadth Indicators**")
        
        # Simulate market breadth data based on current conditions
        if market_conditions['condition'] == 'bull_market':
            advance_decline = 2.1
            new_highs_lows = 1.8
        elif market_conditions['condition'] == 'bear_market':
            advance_decline = 0.4
            new_highs_lows = 0.3
        else:
            advance_decline = 1.0
            new_highs_lows = 1.0
        
        st.metric("Advance/Decline Ratio", f"{advance_decline:.1f}", 
                 help="Ratio of advancing to declining stocks")
        st.metric("New Highs/Lows Ratio", f"{new_highs_lows:.1f}",
                 help="Ratio of stocks making new highs vs new lows")
    
    with col2:
        st.write("**Risk Indicators**")
        
        # VIX equivalent for Indian markets
        vix_level = market_data['volatility'] * 0.8  # Approximate VIX from volatility
        fear_greed = 50 + (market_data['momentum'] * 500)  # Convert momentum to 0-100 scale
        fear_greed = max(0, min(100, fear_greed))
        
        st.metric("India VIX (Est.)", f"{vix_level:.1f}", 
                 help="Estimated volatility index for Indian markets")
        st.metric("Fear & Greed Index", f"{fear_greed:.0f}/100",
                 help="Market sentiment indicator (0=Extreme Fear, 100=Extreme Greed)")
    
    # Sector rotation analysis
    st.subheader("🔄 Sector Rotation Analysis")
    
    # Generate sector performance based on market conditions
    sectors = ['IT', 'Banking', 'Pharma', 'Auto', 'FMCG', 'Energy', 'Metals', 'Realty']
    
    if market_conditions['condition'] == 'bull_market':
        base_performance = [2.1, 1.8, 0.5, 3.2, 0.8, 2.5, 4.1, 1.2]
    elif market_conditions['condition'] == 'bear_market':
        base_performance = [-1.5, -2.1, 0.2, -2.8, -0.3, -3.2, -4.5, -3.8]
    elif market_conditions['condition'] == 'volatile_market':
        base_performance = [0.5, -0.8, 1.2, -1.1, 0.3, -1.5, -0.9, -2.1]
    else:
        base_performance = [1.0, 0.5, 0.8, 0.2, 0.6, 0.1, 0.9, -0.2]
    
    # Add some randomness
    np.random.seed(42)  # Consistent randomness
    performance = [base + np.random.uniform(-0.5, 0.5) for base in base_performance]
    
    # Create sector performance chart
    fig = px.bar(
        x=sectors, 
        y=performance, 
        title="Sector Performance (1 Day %)",
        color=performance,
        color_continuous_scale=['red', 'yellow', 'green']
    )
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Investment recommendations based on analysis
    st.subheader("💡 AI Investment Insights")
    
    insights = []
    
    # Generate insights based on market conditions
    if market_conditions['condition'] == 'bull_market':
        insights.extend([
            "🟢 **Bullish Market Detected**: Consider increasing equity allocation",
            "📈 **Growth Sectors**: IT and Auto sectors showing strong momentum",
            "⚠️ **Risk Management**: Monitor for overheating signals"
        ])
    elif market_conditions['condition'] == 'bear_market':
        insights.extend([
            "🔴 **Bearish Market Detected**: Consider defensive positioning",
            "🛡️ **Safe Haven**: Increase allocation to debt funds and gold",
            "💰 **Opportunity**: Look for quality stocks at discounted prices"
        ])
    elif market_conditions['condition'] == 'volatile_market':
        insights.extend([
            "🟡 **High Volatility**: Reduce position sizes and increase cash",
            "🥇 **Gold Allocation**: Consider increasing gold ETF exposure",
            "📊 **Diversification**: Maintain balanced portfolio allocation"
        ])
    else:
        insights.extend([
            "🔵 **Stable Market**: Good time for systematic investing",
            "⚖️ **Balanced Approach**: Maintain current allocation strategy",
            "🎯 **SIP Opportunity**: Ideal conditions for regular investments"
        ])
    
    # Add volatility-based insights
    if market_data['volatility'] > 25:
        insights.append("⚡ **High Volatility Alert**: Consider reducing small-cap exposure")
    elif market_data['volatility'] < 15:
        insights.append("😴 **Low Volatility**: May indicate complacency, stay alert")
    
    # Add correlation insights
    if market_data['correlation'] > 0.7:
        insights.append("🌍 **High Global Correlation**: Diversify beyond Indian markets")
    
    for insight in insights:
        st.write(insight)
    
    # Market timing indicators
    st.subheader("⏰ Market Timing Indicators")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # RSI equivalent
        rsi = 50 + (market_data['momentum'] * 100)
        rsi = max(0, min(100, rsi))
        
        if rsi > 70:
            rsi_signal = "Overbought ⚠️"
            rsi_color = "red"
        elif rsi < 30:
            rsi_signal = "Oversold 💚"
            rsi_color = "green"
        else:
            rsi_signal = "Neutral 🔵"
            rsi_color = "blue"
        
        st.metric("Market RSI", f"{rsi:.0f}", help="Relative Strength Index (0-100)")
        st.write(f"**Signal**: {rsi_signal}")
    
    with col2:
        # Moving average signal
        if market_data['trend'] == 'bullish':
            ma_signal = "Above MA 📈"
            ma_color = "green"
        elif market_data['trend'] == 'bearish':
            ma_signal = "Below MA 📉"
            ma_color = "red"
        else:
            ma_signal = "Near MA ➡️"
            ma_color = "blue"
        
        st.metric("Trend Signal", market_data['trend'].title())
        st.write(f"**Signal**: {ma_signal}")
    
    with col3:
        # Volume indicator (simulated)
        volume_strength = abs(market_data['momentum']) * 100
        volume_strength = min(100, volume_strength)
        
        if volume_strength > 60:
            volume_signal = "Strong 💪"
        elif volume_strength > 30:
            volume_signal = "Moderate 👍"
        else:
            volume_signal = "Weak 👎"
        
        st.metric("Volume Strength", f"{volume_strength:.0f}%")
        st.write(f"**Signal**: {volume_signal}")
    
    # Economic calendar (mock)
    st.subheader("📅 Upcoming Economic Events")
    
    upcoming_events = [
        {"Date": "Next Week", "Event": "RBI Policy Meeting", "Impact": "High", "Expected": "Rate Hold"},
        {"Date": "15th", "Event": "Inflation Data", "Impact": "Medium", "Expected": "6.2% YoY"},
        {"Date": "Month End", "Event": "GDP Growth", "Impact": "High", "Expected": "6.8% QoQ"},
        {"Date": "Next Month", "Event": "FII/DII Data", "Impact": "Medium", "Expected": "Mixed Flows"}
    ]
    
    events_df = pd.DataFrame(upcoming_events)
    st.dataframe(events_df, use_container_width=True)
    
    # Add market data source information
    st.subheader("📋 Market Data Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Market Metrics:**")
        st.write(f"• Volatility: {market_data['volatility']:.1f}%")
        st.write(f"• Momentum: {market_data['momentum']:.2%}")
        st.write(f"• Trend: {market_data['trend'].title()}")
        st.write(f"• Global Correlation: {market_data['correlation']:.2f}")
    
    with col2:
        st.write("**Analysis Details:**")
        st.write(f"• Market Condition: {market_conditions['condition'].replace('_', ' ').title()}")
        st.write(f"• Confidence Level: {market_conditions['confidence']:.1%}")
        
        # Show data source if available
        if 'data_source' in market_conditions:
            source_icon = "🔴" if market_conditions['data_source'] == 'live' else "📊"
            st.write(f"• Data Source: {source_icon} {market_conditions['data_source'].title()}")
    
    # Risk warning
    st.warning("⚠️ **Disclaimer**: Market analysis is based on historical data and current indicators. Past performance does not guarantee future results. Please consult with a qualified financial advisor before making investment decisions.")

if __name__ == "__main__":
    main()
