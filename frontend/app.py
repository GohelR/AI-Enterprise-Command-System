"""AI Enterprise Operating System - Main Dashboard"""

import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("Starting AI Enterprise Operating System...")

# Configuration
API_BASE_URL = st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", "http://localhost:8000/api/v1"))
REQUEST_TIMEOUT = int(st.secrets.get("REQUEST_TIMEOUT", os.getenv("REQUEST_TIMEOUT", "8")))

# Helper function for API calls with timeout and error handling
def make_api_call(endpoint, method="GET", data=None):
    """Make API call with timeout and error handling"""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=REQUEST_TIMEOUT)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        logger.error(f"API call to {endpoint} timed out")
        st.error("⚠️ Request timed out. Please try again.")
        return None
    except requests.ConnectionError:
        logger.error(f"Could not connect to API at {endpoint}")
        st.warning("⚠️ Backend API is not available. Showing demo mode.")
        return None
    except Exception as e:
        logger.error(f"API call failed: {e}")
        st.error(f"⚠️ Error: {str(e)}")
        return None

logger.info("Initializing Streamlit app configuration...")

def main():
    st.set_page_config(
        page_title="AI Enterprise OS",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    logger.info("App configuration set successfully")

    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            padding: 1rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown('<div class="main-header">🏢 AI Enterprise Operating System</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.radio(
        "Select Department",
        [
            "🏠 Dashboard Overview",
            "👥 Human Resources",
            "💰 Finance & Accounting",
            "💬 Customer Support",
            "📈 Marketing & Growth",
            "🤝 Sales & CRM",
            "🔒 Cybersecurity",
            "📊 Data & Analytics",
            "🤖 AI/ML Models",
            "⚙️ Settings"
        ]
    )

    # Dashboard Overview
    if page == "🏠 Dashboard Overview":
        st.header("Executive Dashboard")

        # Key Metrics
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Total Employees", "1,234", "+12")
        with col2:
            st.metric("Monthly Revenue", "$2.4M", "+18%")
        with col3:
            st.metric("Active Tickets", "89", "-5")
        with col4:
            st.metric("Campaigns", "24", "+3")
        with col5:
            st.metric("Security Alerts", "7", "-2")

        st.markdown("---")

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Revenue Trend")
            # Sample data
            dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
            revenue = [2.0, 2.1, 2.3, 2.2, 2.4, 2.5, 2.7, 2.6, 2.8, 2.9, 3.0, 2.4]
            fig = px.line(x=dates, y=revenue, labels={'x': 'Month', 'y': 'Revenue ($M)'})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📈 Department Performance")
            departments = ['HR', 'Finance', 'Support', 'Marketing', 'Sales', 'IT']
            scores = [85, 92, 78, 88, 90, 86]
            fig = px.bar(x=departments, y=scores, labels={'x': 'Department', 'y': 'Score'})
            st.plotly_chart(fig, use_container_width=True)

        # Department Status
        st.subheader("🏢 Department Status")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("**HR Tech**\n\n✅ Resume Screening: Active\n✅ Retention Model: Running\n⚠️ Performance Review: Due")
        with col2:
            st.info("**Finance**\n\n✅ Fraud Detection: Active\n✅ Revenue Forecast: Updated\n✅ Budget Optimizer: Running")
        with col3:
            st.info("**Customer Support**\n\n✅ AI Chatbot: Online\n✅ Sentiment Analysis: Active\n⚠️ SLA: 2 tickets at risk")

    # Human Resources
    elif page == "👥 Human Resources":
        st.header("Human Resources Tech")

        tab1, tab2, tab3 = st.tabs(["Resume Screening", "Employee Analytics", "Retention Prediction"])

        with tab1:
            st.subheader("📄 AI-Powered Resume Screening")

            candidate_name = st.text_input("Candidate Name")
            candidate_email = st.text_input("Candidate Email")
            resume_text = st.text_area("Paste Resume Text", height=200)

            if st.button("🔍 Screen Resume"):
                if resume_text:
                    with st.spinner("Analyzing resume..."):
                        # Placeholder - would call API
                        score = 75.5
                        status = "Shortlisted"
                        skills = ["Python", "Machine Learning", "AWS", "SQL"]

                        col1, col2, col3 = st.columns(3)
                        col1.metric("AI Score", f"{score}/100")
                        col2.metric("Status", status)
                        col3.metric("Skills Found", len(skills))

                        st.success(f"✅ Resume scored {score}/100 - Status: {status}")
                        st.write("**Extracted Skills:**", ", ".join(skills))
                else:
                    st.warning("Please paste resume text")

        with tab2:
            st.subheader("👔 Employee Performance Analytics")

            # Sample employee data
            employee_data = pd.DataFrame({
                'Employee': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Williams'],
                'Department': ['Engineering', 'Sales', 'Marketing', 'HR'],
                'Performance Score': [88, 92, 85, 90],
                'Retention Risk': [0.2, 0.1, 0.3, 0.15]
            })

            st.dataframe(employee_data, use_container_width=True)

            fig = px.scatter(employee_data, x='Performance Score', y='Retention Risk',
                            size=[100]*len(employee_data), color='Department',
                            hover_data=['Employee'])
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.subheader("🎯 Employee Retention Prediction")

            col1, col2 = st.columns(2)
            with col1:
                performance = st.slider("Performance Score", 0, 100, 75)
                salary = st.number_input("Annual Salary ($)", 30000, 200000, 75000)
            with col2:
                tenure = st.slider("Tenure (years)", 0, 20, 3)

            if st.button("📊 Predict Retention Risk"):
                # Placeholder calculation
                risk = (100 - performance) * 0.3 + max(0, (75000 - salary) / 1000) * 0.1
                risk = min(100, risk) / 100

                st.metric("Retention Risk", f"{risk*100:.1f}%", 
                         delta=f"{'High' if risk > 0.6 else 'Medium' if risk > 0.3 else 'Low'} Risk")

                if risk > 0.6:
                    st.error("⚠️ High retention risk - Immediate action recommended")
                elif risk > 0.3:
                    st.warning("⚡ Medium risk - Schedule check-in")
                else:
                    st.success("✅ Low risk - Employee likely to stay")

    # Finance & Accounting
    elif page == "💰 Finance & Accounting":
        st.header("Finance & Accounting")

        tab1, tab2, tab3 = st.tabs(["Fraud Detection", "Revenue Forecasting", "Budget Optimization"])

        with tab1:
            st.subheader("🔍 Fraud Detection")

            col1, col2 = st.columns(2)
            with col1:
                amount = st.number_input("Transaction Amount ($)", 0.0, 100000.0, 5000.0)
                trans_type = st.selectbox("Type", ["Income", "Expense"])
            with col2:
                description = st.text_input("Description")

            if st.button("🔎 Analyze Transaction"):
                # Placeholder fraud detection
                fraud_score = 0.25 if amount < 10000 else 0.65

                col1, col2 = st.columns(2)
                col1.metric("Fraud Score", f"{fraud_score*100:.1f}%")
                col2.metric("Status", "⚠️ Suspicious" if fraud_score > 0.5 else "✅ Normal")

                if fraud_score > 0.5:
                    st.warning("⚠️ High fraud probability detected - Manual review recommended")

        with tab2:
            st.subheader("📈 Revenue Forecasting")

            # Sample historical data
            historical = [2.0, 2.1, 2.3, 2.2, 2.4, 2.5]

            st.write("**Historical Revenue (Last 6 months):**", historical)

            if st.button("🔮 Generate Forecast"):
                forecast = [2.6, 2.7, 2.8]

                dates = pd.date_range(start='2024-01-01', periods=9, freq='M')
                values = historical + forecast
                types = ['Historical']*6 + ['Forecast']*3

                df = pd.DataFrame({'Date': dates, 'Revenue': values, 'Type': types})
                fig = px.line(df, x='Date', y='Revenue', color='Type')
                st.plotly_chart(fig, use_container_width=True)

                st.success(f"📊 Forecasted revenue: {forecast}")

        with tab3:
            st.subheader("💡 Budget Optimization")

            total_budget = st.number_input("Total Budget ($)", 0, 10000000, 1000000)

            if st.button("⚙️ Optimize Budget"):
                departments = ['HR', 'Marketing', 'Operations', 'R&D', 'Sales']
                allocations = [0.15, 0.25, 0.20, 0.25, 0.15]
                amounts = [total_budget * a for a in allocations]

                df = pd.DataFrame({'Department': departments, 'Allocation': amounts})
                fig = px.pie(df, values='Allocation', names='Department')
                st.plotly_chart(fig, use_container_width=True)

                st.dataframe(df, use_container_width=True)

    # Customer Support
    elif page == "💬 Customer Support":
        st.header("Customer Support & CX")

        tab1, tab2 = st.tabs(["AI Chatbot", "Ticket Analytics"])

        with tab1:
            st.subheader("🤖 AI-Powered Chatbot")

            # Chat interface
            if 'messages' not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            user_input = st.chat_input("Type your message...")

            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})

                # Simple bot response
                if "billing" in user_input.lower():
                    response = "For billing questions, please provide your account number and I'll assist you."
                elif "technical" in user_input.lower() or "error" in user_input.lower():
                    response = "I can help with technical issues. Please describe the problem you're experiencing."
                else:
                    response = "I understand your concern. Let me connect you with the right team member."

                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

        with tab2:
            st.subheader("📊 Ticket Analytics")

            # Sample ticket data
            ticket_data = pd.DataFrame({
                'Ticket ID': ['T001', 'T002', 'T003', 'T004'],
                'Category': ['Technical', 'Billing', 'Account', 'General'],
                'Priority': ['High', 'Medium', 'Low', 'High'],
                'Sentiment': ['Negative', 'Neutral', 'Positive', 'Negative'],
                'Status': ['Open', 'In Progress', 'Resolved', 'Open']
            })

            st.dataframe(ticket_data, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(ticket_data, names='Category', title='Tickets by Category')
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.bar(ticket_data, x='Priority', title='Tickets by Priority')
                st.plotly_chart(fig, use_container_width=True)

    # Marketing & Growth
    elif page == "📈 Marketing & Growth":
        st.header("Marketing & Growth")

        tab1, tab2 = st.tabs(["Lead Scoring", "Campaign Optimization"])

        with tab1:
            st.subheader("🎯 Lead Scoring")

            col1, col2 = st.columns(2)
            with col1:
                lead_name = st.text_input("Lead Name")
                lead_email = st.text_input("Lead Email")
            with col2:
                company = st.text_input("Company")
                source = st.selectbox("Source", ["Referral", "Organic", "Paid", "Social"])

            if st.button("📊 Score Lead"):
                # Placeholder scoring
                score = 75
                probability = 0.65

                col1, col2, col3 = st.columns(3)
                col1.metric("Lead Score", f"{score}/100")
                col2.metric("Conversion Probability", f"{probability*100:.0f}%")
                col3.metric("Status", "🔥 Hot Lead" if score >= 70 else "🌟 Warm")

                st.success("✅ Lead scored successfully")

        with tab2:
            st.subheader("🚀 Campaign Optimization")

            campaign_name = st.text_input("Campaign Name")
            channel = st.selectbox("Channel", ["Email", "Social", "PPC", "SEO"])
            budget = st.number_input("Budget ($)", 0, 100000, 10000)

            if st.button("⚡ Optimize Campaign"):
                st.write("**Optimization Suggestions:**")
                st.write("- A/B test subject lines for higher open rates")
                st.write("- Personalize content based on user segments")
                st.write("- Focus on high-engagement time slots")

                st.metric("Predicted Conversions", "450")
                st.metric("Optimization Score", "87/100")

    # Sales & CRM
    elif page == "🤝 Sales & CRM":
        st.header("Sales & CRM")

        tab1, tab2 = st.tabs(["Customer Health", "Deal Forecasting"])

        with tab1:
            st.subheader("💚 Customer Health Score")

            customer_id = st.text_input("Customer ID")
            col1, col2 = st.columns(2)

            with col1:
                last_activity = st.number_input("Days Since Last Activity", 0, 365, 15)
                support_tickets = st.number_input("Support Tickets", 0, 50, 2)
            with col2:
                engagement = st.slider("Engagement Score", 0, 100, 75)

            if st.button("📊 Analyze Health"):
                churn_risk = 0.25
                health_score = 82
                clv = 15000

                col1, col2, col3 = st.columns(3)
                col1.metric("Health Score", f"{health_score}/100", "Good")
                col2.metric("Churn Risk", f"{churn_risk*100:.0f}%", "Low")
                col3.metric("Lifetime Value", f"${clv:,}")

                st.success("✅ Customer health is good")

        with tab2:
            st.subheader("🎯 Deal Forecasting")

            deal_value = st.number_input("Deal Value ($)", 0, 1000000, 50000)
            stage = st.selectbox("Stage", ["Initial", "Qualified", "Proposal", "Negotiation", "Closing"])

            if st.button("🔮 Forecast Deal"):
                probabilities = {"Initial": 0.1, "Qualified": 0.25, "Proposal": 0.5, "Negotiation": 0.7, "Closing": 0.9}
                prob = probabilities[stage]

                col1, col2 = st.columns(2)
                col1.metric("Close Probability", f"{prob*100:.0f}%")
                col2.metric("Forecast Value", f"${deal_value * prob:,.0f}")

                days_to_close = {"Initial": 60, "Qualified": 45, "Proposal": 30, "Negotiation": 15, "Closing": 7}
                st.info(f"📅 Estimated days to close: {days_to_close[stage]}")

    # Cybersecurity
    elif page == "🔒 Cybersecurity":
        st.header("Cybersecurity & Risk")

        tab1, tab2 = st.tabs(["Security Alerts", "Compliance Monitor"])

        with tab1:
            st.subheader("🚨 Security Alerts")

            # Sample alerts
            alerts = pd.DataFrame({
                'Alert ID': ['A001', 'A002', 'A003'],
                'Type': ['Intrusion', 'Anomaly', 'Breach Attempt'],
                'Severity': ['High', 'Medium', 'Critical'],
                'Source IP': ['192.168.1.100', '10.0.0.50', '203.0.113.45'],
                'Status': ['Open', 'Investigating', 'Resolved']
            })

            st.dataframe(alerts, use_container_width=True)

            st.metric("Open Alerts", "7", "-2")
            st.metric("Critical Alerts", "1", delta_color="inverse")

        with tab2:
            st.subheader("✅ Compliance Monitoring")

            compliance_score = 87
            st.metric("Compliance Score", f"{compliance_score}/100", "Good")

            st.write("**Compliance Status:**")
            st.success("✅ MFA enabled for all users")
            st.success("✅ Encryption at rest enabled")
            st.warning("⚠️ Access review overdue by 5 days")
            st.success("✅ Password policy compliant")

    # Data & Analytics
    elif page == "📊 Data & Analytics":
        st.header("Data & Analytics")

        st.subheader("📈 Business Intelligence Dashboard")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Users", "12,345", "+234")
        col2.metric("Active Projects", "89", "+5")
        col3.metric("Data Processed", "2.3 TB", "+12%")
        col4.metric("API Calls", "1.2M", "+8%")

        st.markdown("---")

        # Sample analytics
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        values = [i * 10 + 100 for i in range(30)]

        df = pd.DataFrame({'Date': dates, 'Metrics': values})
        fig = px.line(df, x='Date', y='Metrics', title='Key Metrics Over Time')
        st.plotly_chart(fig, use_container_width=True)

    # AI/ML Models
    elif page == "🤖 AI/ML Models":
        st.header("AI/ML Model Registry")

        st.subheader("📚 Deployed Models")

        models = pd.DataFrame({
            'Model Name': ['Resume Screener', 'Fraud Detector', 'Churn Predictor', 'Lead Scorer'],
            'Version': ['1.0.0', '1.0.0', '1.0.0', '1.0.0'],
            'Department': ['HR', 'Finance', 'Sales', 'Marketing'],
            'Accuracy': [85.5, 92.3, 88.7, 79.2],
            'Status': ['Active', 'Active', 'Active', 'Active']
        })

        st.dataframe(models, use_container_width=True)

        st.metric("Total Models", "12")
        st.metric("Active Models", "12")
        st.metric("Avg Accuracy", "86.4%")

    # Settings
    elif page == "⚙️ Settings":
        st.header("Settings")

        st.subheader("🔧 System Configuration")

        col1, col2 = st.columns(2)

        with col1:
            st.text_input("API URL", "http://localhost:8000")
            st.selectbox("Environment", ["Development", "Staging", "Production"])

        with col2:
            st.text_input("Database Host", "localhost")
            st.number_input("API Port", 8000, 9000, 8000)

        if st.button("💾 Save Settings"):
            st.success("✅ Settings saved successfully")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>AI Enterprise Operating System v1.0.0 | Built with ❤️ for Enterprise Scale</p>
    </div>
    """, unsafe_allow_html=True)

    # Health check
    if 'app_loaded' not in st.session_state:
        st.session_state.app_loaded = True
        logger.info("App loaded successfully!")
        with st.sidebar:
            st.success("✅ App Loaded Successfully")
    else:
        st.success("✅ App Loaded Successfully")


if __name__ == "__main__":
    logger.info("AI Enterprise Operating System is running...")
    with st.spinner("Loading..."):
        main()
