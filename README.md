# RoboAdvisor Pro - SEBI Compliant Investment Advisory Platform

A comprehensive robo-advisory tool built with Streamlit that creates dynamic investment portfolios for clients based on risk appetite, financial goals, and market conditions. The system uses AI to automatically rebalance portfolios while ensuring compliance with SEBI's Investment Advisor Regulations.

## Features

### 🤖 AI-Powered Portfolio Management
- Dynamic portfolio creation based on client risk profile
- Automated rebalancing using machine learning algorithms
- Real-time market condition analysis
- Optimal asset allocation recommendations

### 📊 Comprehensive Risk Assessment
- Scientific risk profiling questionnaire
- Risk capacity analysis based on financial situation
- Age-appropriate investment recommendations
- Continuous risk monitoring and adjustment

### ⚖️ SEBI Compliance
- Full compliance with SEBI Investment Advisor Regulations
- Automated compliance monitoring and reporting
- Client suitability validation
- Comprehensive audit trail maintenance

### 📈 Advanced Analytics
- Portfolio performance tracking
- Market sentiment analysis
- Sector performance monitoring
- Risk-adjusted returns calculation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd robo-advisor-pro
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
robo-advisor-pro/
├── app.py                 # Main Streamlit application
├── portfolio_manager.py   # Portfolio creation and management
├── risk_profiler.py      # Risk assessment and profiling
├── compliance_checker.py # SEBI compliance monitoring
├── rebalancer.py         # AI-powered rebalancing engine
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Core Components

### Portfolio Manager (`portfolio_manager.py`)
- Creates diversified portfolios based on client profiles
- Manages asset allocation across different risk levels
- Calculates portfolio metrics and performance
- Handles portfolio rebalancing operations

### Risk Profiler (`risk_profiler.py`)
- Conducts comprehensive risk assessment
- Calculates risk scores and categories
- Provides investment recommendations
- Assesses risk capacity based on financial situation

### Compliance Checker (`compliance_checker.py`)
- Monitors SEBI regulatory compliance
- Validates portfolio suitability
- Generates compliance reports
- Maintains audit trails

### AI Rebalancer (`rebalancer.py`)
- Analyzes market conditions using AI
- Detects allocation drift
- Generates rebalancing recommendations
- Simulates rebalancing impact

## SEBI Compliance Features

### Regulatory Requirements
- ✅ Investment Advisor Registration
- ✅ Client Agreement Execution
- ✅ Risk Profiling as per SEBI Guidelines
- ✅ Disclosure Document Provision
- ✅ Transparent Fee Structure
- ✅ Conflict of Interest Management

### Portfolio Compliance
- Maximum single asset exposure limits
- Sector concentration limits
- Minimum diversification requirements
- Small cap exposure limits
- International investment limits

## Usage Guide

### 1. Client Onboarding
- Complete KYC and personal information
- Fill investment profile questionnaire
- Set financial goals and investment horizon
- Determine risk appetite

### 2. Risk Assessment
- Complete comprehensive risk questionnaire
- Review risk score and category
- Get personalized investment recommendations
- Validate risk capacity

### 3. Portfolio Creation
- Automatic portfolio generation based on profile
- Review recommended asset allocation
- Approve portfolio creation
- Monitor initial performance

### 4. AI Rebalancing
- Automatic drift detection
- Market condition analysis
- Rebalancing recommendations
- Impact simulation before execution

### 5. Compliance Monitoring
- Real-time compliance status
- Regulatory requirement tracking
- Audit trail maintenance
- Suitability validation

## Key Features

### Dynamic Asset Allocation
- **Conservative (Low Risk)**: 60-70% Debt, 20-30% Equity, 5-10% Gold
- **Moderate (Medium Risk)**: 30-40% Debt, 50-60% Equity, 5-10% Gold/International
- **Aggressive (High Risk)**: 10-20% Debt, 70-80% Equity, 5-10% International

### AI Rebalancing Triggers
- Allocation drift beyond threshold (5%)
- Market condition changes
- Volatility spikes
- Correlation changes

### Market Analysis
- Real-time market indices tracking
- Sector performance analysis
- Market sentiment indicators
- Volatility monitoring

## Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Market Data**: yfinance
- **Machine Learning**: scikit-learn
- **Date/Time**: datetime

## Compliance Disclaimer

This application is designed to comply with SEBI Investment Advisor Regulations. However, users must ensure:

1. Proper SEBI registration before providing investment advice
2. Execution of client agreements
3. Maintenance of required documentation
4. Regular compliance monitoring
5. Professional indemnity insurance

## Future Enhancements

- Integration with live market data feeds
- Advanced ML models for market prediction
- Mobile application development
- Integration with broking platforms
- Enhanced reporting and analytics
- Multi-language support

## Support

For technical support or compliance queries, please contact:
- Email: [support_email]
- Phone: [support_phone]
- Documentation: [documentation_url]

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Disclaimer**: This is a demonstration application. Please ensure proper SEBI registration and compliance before using for actual investment advisory services.