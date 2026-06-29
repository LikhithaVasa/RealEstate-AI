import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from datetime import datetime

# -------------------------------------------------------
# LOAD CSS
# -------------------------------------------------------

def load_css():

    with open("assets/style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="Risk Analysis",
    page_icon="⚠️",
    layout="wide"
)

# -------------------------------------------------------
# LOAD MODEL
# -------------------------------------------------------

price_model = joblib.load(
    "models/house_price_model.pkl"
)

scaler = joblib.load(
    "models/scaler.pkl"
)

# -------------------------------------------------------
# TITLE
# -------------------------------------------------------

st.markdown("""
<div class="main-title">

⚠️ Property Risk Analysis

</div>

<div class="subtitle">

AI Powered Property Risk Assessment Dashboard

</div>
""",
unsafe_allow_html=True)

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

st.header("🏡 Property Details")

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

    property_age = st.slider(
        "🏠 Property Age (Years)",
        0,
        100,
        25
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

    schools = st.number_input(
        "🏫 Nearby Schools",
        min_value=0,
        max_value=20,
        value=3
    )

    airport_distance = st.slider(
        "✈ Airport Distance (km)",
        0,
        100,
        10
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

    crime_index = st.slider(
        "🚔 Crime Index",
        0,
        100,
        30
    )

# -------------------------------------------------------
# EXTRA RISK FACTORS
# -------------------------------------------------------

st.subheader("🏗 Infrastructure Assessment")

left, right = st.columns(2)

with left:

    infrastructure = st.slider(
        "Infrastructure Score",
        0,
        100,
        75
    )

with right:

    market_growth = st.slider(
        "Market Growth (%)",
        0,
        20,
        8
    )

waterfront = st.checkbox(
    "🌊 Waterfront Property"
)

parking = st.checkbox(
    "🚗 Parking Available",
    value=True
)

st.markdown(
"""
</div>
""",
unsafe_allow_html=True)

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
    "⚠ Analyze Risk",
    use_container_width=True
)
# -------------------------------------------------------
# AI RISK ANALYSIS
# -------------------------------------------------------

if analyze:

    # ---------------------------------------------------
    # Prepare Model Input
    # ---------------------------------------------------

    input_data = pd.DataFrame({

        "number_of_bedrooms":[bedrooms],
        "number_of_bathrooms":[bathrooms],
        "living_area":[living_area],
        "lot_area":[5000],
        "number_of_floors":[1],
        "waterfront_present":[1 if waterfront else 0],
        "number_of_views":[0],
        "condition_of_the_house":[3],
        "grade_of_the_house":[7],
        "house_area_without_basement":[living_area],
        "area_of_the_basement":[0],
        "built_year":[datetime.now().year-property_age],
        "renovation_year":[0],
        "postal_code":[98000],
        "lattitude":[latitude],
        "longitude":[longitude],
        "living_area_renov":[living_area],
        "lot_area_renov":[5000],
        "number_of_schools_nearby":[schools],
        "distance_from_the_airport":[airport_distance],
        "property_age":[property_age]

    })

    # ---------------------------------------------------
    # Predict Property Price
    # ---------------------------------------------------

    scaled = scaler.transform(input_data)

    predicted_price = price_model.predict(
        scaled
    )[0]

    # ---------------------------------------------------
    # GEO SCORE
    # ---------------------------------------------------

    geo_score = (

        schools * 0.25

        +

        infrastructure/100 * 0.30

        +

        (1 if parking else 0) * 0.10

        +

        (1 if waterfront else 0) * 0.10

        -

        airport_distance * 0.003

        -

        crime_index/100 * 0.25

    )

    geo_score = max(
        0,
        min(
            geo_score,
            1
        )
    )

    # ---------------------------------------------------
    # RISK SCORE
    # ---------------------------------------------------

    risk_score = (

        property_age * 0.25

        +

        airport_distance * 0.15

        +

        crime_index * 0.35

        +

        (100-infrastructure) * 0.15

        +

        (20-schools) * 0.10

    )

    risk_score = round(

        max(
            0,
            min(
                risk_score,
                100
            )
        ),

        1

    )

    # ---------------------------------------------------
    # MARKET STABILITY
    # ---------------------------------------------------

    market_stability = round(

        infrastructure*0.5

        +

        market_growth*2

        +

        schools*2

        -

        crime_index*0.2,

        1

    )

    market_stability = max(
        0,
        min(
            market_stability,
            100
        )
    )

    # ---------------------------------------------------
    # RISK CATEGORY
    # ---------------------------------------------------

    if risk_score < 35:

        risk_category = "🟢 LOW RISK"

        color = "#22c55e"

    elif risk_score < 65:

        risk_category = "🟡 MEDIUM RISK"

        color = "#facc15"

    else:

        risk_category = "🔴 HIGH RISK"

        color = "#ef4444"

    # ---------------------------------------------------
    # METRICS
    # ---------------------------------------------------

    st.divider()

    st.header("⚠ AI Risk Assessment Report")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "🏠 Property Value",
            f"${predicted_price:,.0f}"
        )

    with c2:

        st.metric(
            "⚠ Risk Score",
            f"{risk_score}/100"
        )

    with c3:

        st.metric(
            "🌍 Geo Score",
            f"{geo_score:.2f}"
        )

    with c4:

        st.metric(
            "📈 Market Stability",
            f"{market_stability}"
        )

    st.write("")

    # ---------------------------------------------------
    # PROGRESS BAR
    # ---------------------------------------------------

    st.subheader("Risk Level")

    st.progress(risk_score/100)

    st.write(f"### {risk_category}")

    # ---------------------------------------------------
    # PLOTLY GAUGE
    # ---------------------------------------------------

    gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=risk_score,

            title={"text":"Property Risk Score"},

            gauge={

                "axis":{"range":[0,100]},

                "bar":{"color":color},

                "steps":[

                    {"range":[0,35],"color":"#14532d"},

                    {"range":[35,65],"color":"#854d0e"},

                    {"range":[65,100],"color":"#7f1d1d"}

                ]

            }

        )

    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )
    # ---------------------------------------------------
    # RISK DISTRIBUTION
    # ---------------------------------------------------

    st.subheader("📊 Risk Factor Distribution")

    risk_labels = [
        "Crime",
        "Property Age",
        "Airport Distance",
        "Infrastructure",
        "Schools"
    ]

    risk_values = [

        crime_index,

        property_age,

        airport_distance,

        100 - infrastructure,

        20 - schools

    ]

    pie = go.Figure(

        data=[

            go.Pie(

                labels=risk_labels,

                values=risk_values,

                hole=0.45

            )

        ]

    )

    pie.update_layout(
        height=450
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

    # ---------------------------------------------------
    # AI RISK EXPLANATION
    # ---------------------------------------------------

    st.subheader("🤖 AI Risk Explanation")

    explanations = []

    if crime_index > 70:
        explanations.append("❌ High crime index significantly increases investment risk.")
    elif crime_index > 40:
        explanations.append("⚠ Moderate crime index contributes to medium risk.")
    else:
        explanations.append("✅ Low crime index improves investment safety.")

    if property_age > 40:
        explanations.append("⚠ Older properties may require higher maintenance.")
    elif property_age < 15:
        explanations.append("✅ Newer property reduces maintenance risk.")

    if airport_distance < 15:
        explanations.append("✅ Excellent connectivity to the airport.")
    elif airport_distance > 50:
        explanations.append("⚠ Long airport distance reduces accessibility.")

    if infrastructure > 80:
        explanations.append("✅ Excellent infrastructure supports future appreciation.")
    elif infrastructure < 40:
        explanations.append("⚠ Poor infrastructure increases investment risk.")

    if schools >= 5:
        explanations.append("✅ Good educational facilities increase property demand.")
    else:
        explanations.append("⚠ Limited nearby schools reduce attractiveness.")

    if waterfront:
        explanations.append("✅ Waterfront properties generally appreciate faster.")

    if parking:
        explanations.append("✅ Parking availability increases resale value.")

    for item in explanations:
        st.success(item)

    # ---------------------------------------------------
    # FINAL RECOMMENDATION
    # ---------------------------------------------------

    st.markdown(
        f"""
        <div style="
        background:#111827;
        padding:25px;
        border-radius:15px;
        border-left:8px solid {color};
        box-shadow:0px 8px 20px rgba(0,0,0,0.35);
        ">

        <h2 style="color:white;">
        🛡 Final Risk Assessment
        </h2>

        <h1 style="color:{color};">
        {risk_category}
        </h1>

        <h3 style="color:white;">
        Overall Risk Score : {risk_score}/100
        </h3>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # DOWNLOAD REPORT
    # ---------------------------------------------------

    report = f"""
AI POWERED REAL ESTATE INTELLIGENCE PLATFORM

==================================

PROPERTY RISK REPORT

==================================

Predicted Property Price

${predicted_price:,.2f}

Risk Score

{risk_score}/100

Risk Category

{risk_category}

Geo Score

{geo_score:.2f}

Market Stability

{market_stability}/100

Crime Index

{crime_index}

Infrastructure Score

{infrastructure}

Nearby Schools

{schools}

Airport Distance

{airport_distance} km

Property Age

{property_age} years

Generated using AI Powered Real Estate Intelligence Platform
"""

    st.download_button(
        "📄 Download Risk Report",
        report,
        file_name="Risk_Report.txt",
        use_container_width=True
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "© 2026 AI Powered Real Estate Intelligence Platform | Risk Analysis Dashboard"
)