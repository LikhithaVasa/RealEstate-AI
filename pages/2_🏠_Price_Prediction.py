import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from datetime import datetime

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="Property Price Prediction",
    page_icon="🏠",
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

🏠 AI Property Price Prediction

</div>

<div class="subtitle">

Machine Learning Based Real Estate Valuation

</div>
""",
unsafe_allow_html=True)

st.write("")

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

with st.sidebar:

    st.title("🏠 Price Prediction")

    st.success("Random Forest Model")

    st.info(
        """
Model Accuracy

R² Score : 87.6%

MAE : 50,957

RMSE : 73,725
"""
    )

    st.divider()

    st.write(
        """
### Prediction Steps

✅ Enter property details

✅ Click Analyze

✅ View AI report

✅ Download report
"""
    )

# -------------------------------------------------------
# INPUT CARD
# -------------------------------------------------------

st.markdown(
"""
<div class="card">
""",
unsafe_allow_html=True
)

st.header("🏡 Property Information")

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
# EXTRA PROPERTY DETAILS
# -------------------------------------------------------

st.markdown(
"""
<div class="card">
""",
unsafe_allow_html=True
)

st.subheader("🏠 Additional Property Details")

c1, c2, c3 = st.columns(3)

with c1:

    property_age = st.slider(
        "Property Age",
        0,
        100,
        25
    )

with c2:

    condition = st.selectbox(
        "House Condition",
        [1,2,3,4,5]
    )

with c3:

    grade = st.selectbox(
        "House Grade",
        [1,2,3,4,5,6,7,8,9,10]
    )

waterfront = st.checkbox(
    "Waterfront Property"
)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# MAP
# -------------------------------------------------------

st.subheader("📍 Property Location")

map_df = pd.DataFrame(
    {
        "lat":[latitude],
        "lon":[longitude]
    }
)

st.map(map_df)

st.write("")

# -------------------------------------------------------
# ANALYZE BUTTON
# -------------------------------------------------------

analyze = st.button(
    "🚀 Analyze Property",
    use_container_width=True
)
# -------------------------------------------------------
# PREDICTION
# -------------------------------------------------------

if analyze:

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


    scaled = scaler.transform(input_data)

    predicted_price = price_model.predict(scaled)[0]



    # ---------------------------------------------
    # Geo Score
    # ---------------------------------------------

    geo_score = (

        schools*0.25

        +

        (1 if waterfront else 0)*0.25

        -

        airport_distance*0.003

    )

    geo_score = max(0,min(geo_score,1))



    # ---------------------------------------------
    # Investment Score
    # ---------------------------------------------

    investment_score = (

        geo_score*40

        +

        (grade/10)*30

        +

        (living_area/5000)*20

        +

        (bedrooms/10)*10

    )



    investment_score = min(
        investment_score,
        100
    )



    # ---------------------------------------------
    # Recommendation
    # ---------------------------------------------

    if investment_score >= 70:

        recommendation = "🚀 BUY"

        color="green"

    elif investment_score >= 45:

        recommendation = "👍 HOLD"

        color="orange"

    else:

        recommendation = "⚠ SELL"

        color="red"



    # ---------------------------------------------
    # AI Report
    # ---------------------------------------------

    st.divider()

    st.header("🤖 AI Property Report")



    c1,c2,c3 = st.columns(3)



    with c1:

        st.metric(

            "🏠 Estimated Price",

            f"${predicted_price:,.0f}"

        )



    with c2:

        st.metric(

            "🌍 Geo Score",

            f"{geo_score:.2f}"

        )



    with c3:

        st.metric(

            "📈 Investment Score",

            f"{investment_score:.1f}/100"

        )



    st.write("")



    st.subheader("Investment Score")

    st.progress(
        investment_score/100
    )



    st.subheader("Geo Score")

    st.progress(
        geo_score
    )



    st.write("")



    # ---------------------------------------------
    # Recommendation Card
    # ---------------------------------------------

    st.markdown(f"""

<div style='
padding:30px;
border-radius:20px;
background:#111827;
border:2px solid {color};
text-align:center;
'>

<h2>Final Recommendation</h2>

<h1>{recommendation}</h1>

</div>

""",
unsafe_allow_html=True)



    st.write("")



    # ---------------------------------------------
    # AI Explanation
    # ---------------------------------------------

    st.markdown("""
<div class="card">
""",
unsafe_allow_html=True)



    st.subheader("🧠 AI Decision Summary")



    reasons=[]



    if grade>=7:

        reasons.append("✔ Premium quality construction")



    if schools>=5:

        reasons.append("✔ Excellent educational facilities nearby")



    if waterfront:

        reasons.append("✔ Waterfront property adds value")



    if property_age<15:

        reasons.append("✔ Relatively newer property")



    if airport_distance<15:

        reasons.append("✔ Close to transportation hub")



    if len(reasons)==0:

        reasons.append("✔ Standard residential property")



    for r in reasons:

        st.success(r)



    st.markdown("</div>",unsafe_allow_html=True)



    st.write("")



    # ---------------------------------------------
    # Download Report
    # ---------------------------------------------

    report=f"""
AI PROPERTY REPORT
==============================

Estimated Price :
${predicted_price:,.2f}

Geo Score :
{geo_score:.2f}

Investment Score :
{investment_score:.1f}

Recommendation :
{recommendation}

Bedrooms :
{bedrooms}

Bathrooms :
{bathrooms}

Living Area :
{living_area}

Schools :
{schools}

Airport Distance :
{airport_distance}

Property Age :
{property_age}

Generated using
AI Powered Real Estate Intelligence Platform
"""



    st.download_button(

        "📄 Download Property Report",

        report,

        file_name="AI_Property_Report.txt"

    )



st.divider()

st.caption(

"AI Powered Real Estate Intelligence Platform | Price Prediction Dashboard"

)