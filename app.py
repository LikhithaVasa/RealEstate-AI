import streamlit as st

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Real Estate Intelligence",
    page_icon="🏠",
    layout="wide"
)

# ---------------- LOAD CSS ----------------

def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# ---------------- HERO ----------------

st.markdown("""
<div class="main-title">

🏠 AI-Powered Real Estate Intelligence Platform

</div>

<div class="subtitle">

Smart Property Valuation • Investment Intelligence • Risk Analysis • Future Forecasting

</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- OVERVIEW ----------------

st.markdown("""
<div class="card">

## 📌 Project Overview

This platform uses Artificial Intelligence and Machine Learning to help buyers,
investors, and real estate professionals make smarter property decisions.

The system provides:

- Property Price Prediction
- Investment Recommendation
- Geo Risk Analysis
- Future Price Forecasting
- Explainable AI (SHAP)
- Property Comparison
- Market Insights Dashboard

</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- FEATURES ----------------

st.header("🚀 Platform Features")

col1, col2 = st.columns(2)

with col1:

    st.success("🏠 AI Property Price Prediction")

    st.success("🌍 Geo Risk Analysis")

    st.success("📈 Investment Recommendation")

    st.success("⚠️ Property Risk Assessment")

with col2:

    st.success("🔮 Future Price Forecast")

    st.success("🤖 Explainable AI (SHAP)")

    st.success("⚖️ Property Comparison")

    st.success("📊 Market Insights Dashboard")

st.write("")

# ---------------- PROJECT STATS ----------------

st.header("📊 Project Statistics")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Properties", "15,000+")

with m2:
    st.metric("ML Models", "6")

with m3:
    st.metric("Model Accuracy", "87.6%")

with m4:
    st.metric("Dashboard Pages", "8")

st.write("")

# ---------------- TECHNOLOGY ----------------

st.header("🛠 Technology Stack")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.info("""
🐍 Python

🐼 Pandas

🔢 NumPy

📊 Scikit-Learn
""")

with tech2:
    st.info("""
⚡ XGBoost

🌳 LightGBM

🐱 CatBoost

📈 Plotly
""")

with tech3:
    st.info("""
🤖 SHAP

🎨 Streamlit

💾 Joblib

📂 CSV Dataset
""")

st.write("")

# ---------------- HOW TO USE ----------------

st.header("📖 How to Use")

st.markdown("""
1️⃣ Select a dashboard page from the **left sidebar**.

2️⃣ Enter the required property information.

3️⃣ Click **Analyze** or **Predict**.

4️⃣ Explore AI-generated insights, investment scores, risk analysis, and forecasts.
""")

st.write("")

st.info("👈 Use the navigation menu in the left sidebar to explore all dashboard pages.")

st.divider()

st.caption(
    "AI-Powered Real Estate Intelligence Platform | Developed using Python, Machine Learning and Streamlit"
)