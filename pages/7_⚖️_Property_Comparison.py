import streamlit as st
import pandas as pd

# =========================
# Page Config
# =========================

st.set_page_config(
    page_title="Property Comparison",
    page_icon="⚖️",
    layout="wide"
)

# =========================
# Load CSS
# =========================

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.title("⚖️ Property Comparison")

st.markdown("""
Compare two properties side by side to identify the
better investment opportunity.
""")

# =========================
# Load Dataset
# =========================

@st.cache_data
def load_data():
    return pd.read_csv(
        "dataset/processed/future_price_forecast.csv"
    )

df = load_data()

# =========================
# Property Selection
# =========================

col1, col2 = st.columns(2)

with col1:
    property_a = st.selectbox(
        "Select Property A",
        df["id"],
        key="A"
    )

with col2:
    property_b = st.selectbox(
        "Select Property B",
        df["id"],
        index=1,
        key="B"
    )

prop_a = df[df["id"] == property_a].iloc[0]
prop_b = df[df["id"] == property_b].iloc[0]

# =========================
# Comparison Table
# =========================

comparison = pd.DataFrame({
    "Feature": [
        "Price",
        "Bedrooms",
        "Bathrooms",
        "Living Area",
        "Property Age",
        "Growth Score",
        "Annual Growth Rate",
        "Price After 5 Years"
    ],
    "Property A": [
        prop_a["price"],
        prop_a["number_of_bedrooms"],
        prop_a["number_of_bathrooms"],
        prop_a["living_area"],
        prop_a["property_age"],
        prop_a["growth_score"],
        prop_a["annual_growth_rate"],
        prop_a["price_after_5_years"]
    ],
    "Property B": [
        prop_b["price"],
        prop_b["number_of_bedrooms"],
        prop_b["number_of_bathrooms"],
        prop_b["living_area"],
        prop_b["property_age"],
        prop_b["growth_score"],
        prop_b["annual_growth_rate"],
        prop_b["price_after_5_years"]
    ]
})

st.subheader("📋 Property Comparison")

st.dataframe(
    comparison,
    use_container_width=True
)
import plotly.express as px

# =========================
# Comparison Charts
# =========================

st.markdown("---")
st.subheader("📊 Visual Comparison")

comparison_chart = pd.DataFrame({
    "Property": ["Property A", "Property B"],
    "Current Price": [prop_a["price"], prop_b["price"]],
    "5-Year Price": [prop_a["price_after_5_years"], prop_b["price_after_5_years"]],
    "Growth Score": [prop_a["growth_score"], prop_b["growth_score"]]
})

# Current Price Chart
fig1 = px.bar(
    comparison_chart,
    x="Property",
    y="Current Price",
    title="Current Property Price Comparison",
    text_auto=".2s"
)

fig1.update_layout(template="plotly_dark")

st.plotly_chart(fig1, use_container_width=True)

# Future Price Chart
fig2 = px.bar(
    comparison_chart,
    x="Property",
    y="5-Year Price",
    title="Predicted Price After 5 Years",
    text_auto=".2s"
)

fig2.update_layout(template="plotly_dark")

st.plotly_chart(fig2, use_container_width=True)

# Growth Score Chart
fig3 = px.bar(
    comparison_chart,
    x="Property",
    y="Growth Score",
    title="Growth Score Comparison",
    text_auto=".2f"
)

fig3.update_layout(template="plotly_dark")

st.plotly_chart(fig3, use_container_width=True)


# =========================
# AI Recommendation
# =========================

st.markdown("---")
st.subheader("🤖 AI Investment Recommendation")

score_a = (
    prop_a["growth_score"] * 0.5 +
    prop_a["annual_growth_rate"] * 0.3 +
    ((prop_a["price_after_5_years"] - prop_a["price"]) / prop_a["price"] * 100) * 0.2
)

score_b = (
    prop_b["growth_score"] * 0.5 +
    prop_b["annual_growth_rate"] * 0.3 +
    ((prop_b["price_after_5_years"] - prop_b["price"]) / prop_b["price"] * 100) * 0.2
)

if score_a > score_b:
    winner = "🏆 Property A"
    explanation = (
        "Property A has a stronger overall investment profile "
        "based on growth score, annual growth rate, and projected appreciation."
    )
else:
    winner = "🏆 Property B"
    explanation = (
        "Property B has a stronger overall investment profile "
        "based on growth score, annual growth rate, and projected appreciation."
    )

st.success(f"### Recommended Investment: {winner}")

st.info(explanation)


# =========================
# Download Comparison
# =========================

st.markdown("---")

csv = comparison.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Comparison Report",
    data=csv,
    file_name="property_comparison.csv",
    mime="text/csv"
)