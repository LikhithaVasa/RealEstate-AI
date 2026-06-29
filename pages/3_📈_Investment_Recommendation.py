import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="Investment Recommendation",
    page_icon="📈",
    layout="wide"
)

# -------------------------------------------------------
# LOAD CSS
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

css_path = BASE_DIR / "assets" / "style.css"

with open(css_path) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# -------------------------------------------------------
# LOAD MODELS
# -------------------------------------------------------

price_model = joblib.load(
    BASE_DIR / "models" / "house_price_model.pkl"
)

scaler = joblib.load(
    BASE_DIR / "models" / "scaler.pkl"
)

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.markdown("""
<div class="main-title">

📈 AI Investment Recommendation

</div>

<div class="subtitle">

Smart Property Investment Intelligence Platform

</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

with st.sidebar:

    st.title("📈 Investment AI")

    st.success("AI Recommendation Engine")

    st.info("""
### Features

✅ Price Prediction

✅ Investment Score

✅ ROI Estimation

✅ BUY / HOLD / SELL

✅ AI Decision Summary
""")

    st.divider()

    st.markdown("""
### Investment Grades

🟢 **A+** Excellent

🟢 **A** Very Good

🟡 **B** Moderate

🟠 **C** Average

🔴 **D** High Risk
""")

    st.divider()

    st.metric(
        "Model Accuracy",
        "87.6%"
    )

# -------------------------------------------------------
# PAGE INTRODUCTION
# -------------------------------------------------------

st.markdown("""
<div class="card">

## 📊 Investment Recommendation Dashboard

This dashboard evaluates a property using Machine Learning,
geographical intelligence and investment analytics.

It estimates:

- 💰 Property Value
- 📈 Investment Score
- 💵 Estimated ROI
- 🌍 Location Quality
- ⚠ Risk Level
- 🏆 Final Recommendation

</div>
""", unsafe_allow_html=True)

st.write("")
# -------------------------------------------------------
# PROPERTY DETAILS
# -------------------------------------------------------

st.markdown(
"""
<div class="card">
""",
unsafe_allow_html=True
)

st.header("🏡 Investment Property Details")

col1, col2, col3 = st.columns(3)

# -------------------------------------------------------
# COLUMN 1
# -------------------------------------------------------

with col1:

    bedrooms = st.number_input(
        "🛏 Bedrooms",
        min_value=1,
        max_value=10,
        value=3
    )

    bathrooms = st.number_input(
        "🚿 Bathrooms",
        min_value=1,
        max_value=10,
        value=2
    )

    floors = st.number_input(
        "🏢 Floors",
        min_value=1,
        max_value=5,
        value=1
    )

# -------------------------------------------------------
# COLUMN 2
# -------------------------------------------------------

with col2:

    living_area = st.number_input(
        "📐 Living Area (sqft)",
        min_value=300,
        max_value=15000,
        value=1500
    )

    lot_area = st.number_input(
        "🌳 Lot Area (sqft)",
        min_value=500,
        max_value=50000,
        value=5000
    )

    schools = st.number_input(
        "🏫 Nearby Schools",
        min_value=0,
        max_value=20,
        value=3
    )

# -------------------------------------------------------
# COLUMN 3
# -------------------------------------------------------

with col3:

    latitude = st.number_input(
        "🌍 Latitude",
        value=47.5,
        format="%.4f"
    )

    longitude = st.number_input(
        "🌍 Longitude",
        value=-122.2,
        format="%.4f"
    )

    airport_distance = st.slider(
        "✈ Airport Distance (km)",
        0,
        100,
        10
    )

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# ADDITIONAL PROPERTY DETAILS
# -------------------------------------------------------

st.markdown(
"""
<div class="card">
""",
unsafe_allow_html=True
)

st.subheader("🏠 Additional Property Information")

c1, c2, c3 = st.columns(3)

with c1:

    property_age = st.slider(
        "Property Age (Years)",
        0,
        100,
        25
    )

with c2:

    condition = st.selectbox(
        "House Condition",
        [1, 2, 3, 4, 5],
        index=2
    )

with c3:

    grade = st.selectbox(
        "House Grade",
        [1,2,3,4,5,6,7,8,9,10],
        index=6
    )

waterfront = st.checkbox(
    "🌊 Waterfront Property"
)

parking = st.checkbox(
    "🚗 Parking Available",
    value=True
)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# INVESTMENT ASSUMPTIONS
# -------------------------------------------------------

st.markdown(
"""
<div class="card">
""",
unsafe_allow_html=True
)

st.subheader("💰 Investment Assumptions")

a, b, c = st.columns(3)

with a:

    purchase_cost = st.number_input(
        "Purchase Cost ($)",
        value=500000,
        step=10000
    )

with b:

    expected_rent = st.number_input(
        "Expected Monthly Rent ($)",
        value=2500,
        step=100
    )

with c:

    yearly_growth = st.slider(
        "Expected Annual Growth (%)",
        0,
        20,
        8
    )

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# PROPERTY LOCATION
# -------------------------------------------------------

st.subheader("📍 Property Location")

map_df = pd.DataFrame(
    {
        "lat": [latitude],
        "lon": [longitude]
    }
)

st.map(map_df)

st.write("")

# -------------------------------------------------------
# ANALYZE BUTTON
# -------------------------------------------------------

analyze = st.button(
    "📈 Analyze Investment",
    use_container_width=True
)
# -------------------------------------------------------
# AI INVESTMENT ANALYSIS
# -------------------------------------------------------

if analyze:

    # ---------------------------------------------
    # Create Input Data
    # ---------------------------------------------

    input_data = pd.DataFrame({

        "number_of_bedrooms":[bedrooms],
        "number_of_bathrooms":[bathrooms],
        "living_area":[living_area],
        "lot_area":[lot_area],
        "number_of_floors":[floors],
        "waterfront_present":[1 if waterfront else 0],
        "number_of_views":[0],
        "condition_of_the_house":[condition],
        "grade_of_the_house":[grade],
        "house_area_without_basement":[living_area],
        "area_of_the_basement":[0],
        "built_year":[datetime.now().year-property_age],
        "renovation_year":[0],
        "postal_code":[98000],
        "lattitude":[latitude],
        "longitude":[longitude],
        "living_area_renov":[living_area],
        "lot_area_renov":[lot_area],
        "number_of_schools_nearby":[schools],
        "distance_from_the_airport":[airport_distance],
        "property_age":[property_age]

    })

    # ---------------------------------------------
    # Prediction
    # ---------------------------------------------

    scaled = scaler.transform(input_data)

    predicted_price = price_model.predict(scaled)[0]

    # ---------------------------------------------
    # Geo Score
    # ---------------------------------------------

    geo_score = (

        schools*0.22

        +

        (1 if waterfront else 0)*0.25

        +

        (1 if parking else 0)*0.08

        -

        airport_distance*0.003

    )

    geo_score = max(
        0,
        min(
            geo_score,
            1
        )
    )

    # ---------------------------------------------
    # Investment Score
    # ---------------------------------------------

    investment_score = (

        geo_score*35

        +

        (grade/10)*25

        +

        (living_area/5000)*20

        +

        (bedrooms/10)*10

        +

        (yearly_growth/20)*10

    )

    investment_score = round(
        min(
            investment_score,
            100
        ),
        1
    )

    # ---------------------------------------------
    # ROI
    # ---------------------------------------------

    annual_rent = expected_rent * 12

    roi = round(

        (annual_rent / purchase_cost) * 100,

        2

    )

    appreciation = round(

        purchase_cost *

        yearly_growth / 100,

        2

    )

    # ---------------------------------------------
    # Risk Score
    # ---------------------------------------------

    risk_score = round(

        100 - investment_score,

        1

    )

    if risk_score < 30:

        risk = "Low"

    elif risk_score < 60:

        risk = "Medium"

    else:

        risk = "High"

    # ---------------------------------------------
    # BUY HOLD SELL
    # ---------------------------------------------

    if investment_score >= 75:

        recommendation = "🟢 BUY"

        grade_text = "A+"

        color = "#22c55e"

    elif investment_score >= 60:

        recommendation = "🟡 HOLD"

        grade_text = "A"

        color = "#eab308"

    elif investment_score >= 45:

        recommendation = "🟠 HOLD"

        grade_text = "B"

        color = "#f97316"

    else:

        recommendation = "🔴 SELL"

        grade_text = "C"

        color = "#ef4444"

    # ---------------------------------------------
    # REPORT TITLE
    # ---------------------------------------------

    st.divider()

    st.header("📈 AI Investment Report")

    # ---------------------------------------------
    # METRICS
    # ---------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "🏠 Property Value",
            f"${predicted_price:,.0f}"
        )

    with c2:

        st.metric(
            "📈 Investment Score",
            f"{investment_score}"
        )

    with c3:

        st.metric(
            "💵 ROI",
            f"{roi}%"
        )

    with c4:

        st.metric(
            "⚠ Risk",
            risk
        )

    st.write("")

    # ---------------------------------------------
    # INVESTMENT SCORE
    # ---------------------------------------------

    st.subheader("📈 Investment Score")

    st.progress(
        investment_score/100
    )

    st.write(
        f"**Investment Grade : {grade_text}**"
    )

    # ---------------------------------------------
    # GAUGE CHART
    # ---------------------------------------------

    gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=investment_score,

            title={'text':"Investment Score"},

            gauge={

                'axis':{'range':[0,100]},

                'bar':{'color':color},

                'steps':[

                    {'range':[0,40],'color':"#7f1d1d"},

                    {'range':[40,70],'color':"#854d0e"},

                    {'range':[70,100],'color':"#14532d"}

                ]

            }

        )

    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )
    # -------------------------------------------------------
    # RECOMMENDATION CARD
    # -------------------------------------------------------

    st.write("")

    st.markdown(
        f"""
        <div style="
        background-color:#111827;
        border-left:8px solid {color};
        padding:25px;
        border-radius:15px;
        box-shadow:0px 8px 20px rgba(0,0,0,0.35);
        ">

        <h2 style="color:white;">🏆 Final Recommendation</h2>

        <h1 style="color:{color};">{recommendation}</h1>

        <h3 style="color:white;">
        Investment Grade : {grade_text}
        </h3>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # -------------------------------------------------------
    # INVESTMENT SUMMARY
    # -------------------------------------------------------

    st.subheader("💰 Investment Summary")

    s1, s2, s3 = st.columns(3)

    with s1:

        st.metric(
            "Annual Rental Income",
            f"${annual_rent:,.0f}"
        )

    with s2:

        st.metric(
            "Expected Appreciation",
            f"${appreciation:,.0f}"
        )

    with s3:

        st.metric(
            "Risk Score",
            f"{risk_score}/100"
        )

    st.write("")

    # -------------------------------------------------------
    # ROI BAR
    # -------------------------------------------------------

    st.subheader("📊 Investment Indicators")

    st.write("Investment Score")
    st.progress(investment_score / 100)

    st.write("ROI")
    st.progress(min(roi / 20, 1.0))

    st.write("Location Quality")
    st.progress(geo_score)

    st.write("")

    # -------------------------------------------------------
    # AI DECISION SUMMARY
    # -------------------------------------------------------

    st.markdown("""
    <div class="card">
    """, unsafe_allow_html=True)

    st.subheader("🧠 AI Decision Summary")

    reasons = []

    if investment_score >= 75:
        reasons.append("✅ Excellent investment opportunity.")

    if grade >= 8:
        reasons.append("✅ Premium quality construction.")

    elif grade >= 6:
        reasons.append("✅ Good construction quality.")

    if schools >= 5:
        reasons.append("✅ Good educational facilities nearby.")

    if waterfront:
        reasons.append("✅ Waterfront property increases resale value.")

    if parking:
        reasons.append("✅ Parking improves long-term demand.")

    if property_age <= 10:
        reasons.append("✅ Relatively new property.")

    elif property_age <= 25:
        reasons.append("✅ Moderate property age.")

    else:
        reasons.append("⚠ Older property may require maintenance.")

    if airport_distance <= 15:
        reasons.append("✅ Good transportation connectivity.")

    elif airport_distance >= 50:
        reasons.append("⚠ Property is far from airport.")

    if roi >= 10:
        reasons.append("✅ Strong rental return.")

    elif roi >= 6:
        reasons.append("✅ Average rental return.")

    else:
        reasons.append("⚠ Rental return is relatively low.")

    if risk == "Low":
        reasons.append("✅ Low investment risk.")

    elif risk == "Medium":
        reasons.append("⚠ Medium investment risk.")

    else:
        reasons.append("❌ High investment risk.")

    for item in reasons:
        st.success(item)

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # -------------------------------------------------------
    # REPORT
    # -------------------------------------------------------

    report = f"""
AI POWERED REAL ESTATE INTELLIGENCE PLATFORM

======================================

INVESTMENT REPORT

======================================

Predicted Property Price

${predicted_price:,.2f}

Investment Score

{investment_score}/100

Investment Grade

{grade_text}

Recommendation

{recommendation}

Estimated ROI

{roi}%

Annual Rental Income

${annual_rent:,.2f}

Expected Appreciation

${appreciation:,.2f}

Risk Level

{risk}

Bedrooms : {bedrooms}

Bathrooms : {bathrooms}

Living Area : {living_area}

Schools Nearby : {schools}

Airport Distance : {airport_distance} km

Property Age : {property_age} years

Generated using

AI Powered Real Estate Intelligence Platform
"""

    st.download_button(
        "📄 Download Investment Report",
        report,
        file_name="Investment_Report.txt",
        use_container_width=True
    )

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------

st.divider()

st.caption(
    "© 2026 AI Powered Real Estate Intelligence Platform | Investment Recommendation Dashboard"
)