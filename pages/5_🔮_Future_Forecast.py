import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="Future Forecast",
    page_icon="🔮",
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

# =========================
# Title
# =========================

st.title("🔮 Future Property Price Forecast")

st.markdown(
"""
Analyze future property appreciation using the
precomputed forecasting dataset.
"""
)

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

st.subheader("🏠 Select Property")

property_id = st.selectbox(
    "Choose Property ID",
    df["id"].tolist()
)

property_data = df[df["id"] == property_id].iloc[0]

# =========================
# Property Overview
# =========================

st.subheader("📋 Property Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Bedrooms",
        int(property_data["number_of_bedrooms"])
    )

    st.metric(
        "Bathrooms",
        int(property_data["number_of_bathrooms"])
    )

with col2:
    st.metric(
        "Living Area",
        f"{property_data['living_area']:,} sq.ft"
    )

    st.metric(
        "Property Age",
        int(property_data["property_age"])
    )

with col3:
    st.metric(
        "Current Price",
        f"₹ {property_data['price']:,.0f}"
    )

    st.metric(
        "Growth Score",
        round(property_data["growth_score"], 2)
    )
# =========================
# Future Price Forecast
# =========================

st.markdown("---")
st.subheader("📈 Future Price Forecast")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="💰 Price After 1 Year",
        value=f"₹ {property_data['price_after_1_year']:,.0f}"
    )

with col2:
    st.metric(
        label="💰 Price After 3 Years",
        value=f"₹ {property_data['price_after_3_years']:,.0f}"
    )

with col3:
    st.metric(
        label="💰 Price After 5 Years",
        value=f"₹ {property_data['price_after_5_years']:,.0f}"
    )


# =========================
# Growth Details
# =========================

st.markdown("---")
st.subheader("📊 Growth Analysis")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="📈 Annual Growth Rate",
        value=f"{property_data['annual_growth_rate']:.2f}%"
    )

with col2:
    st.metric(
        label="⭐ Growth Score",
        value=f"{property_data['growth_score']:.2f}"
    )
# =========================
# Forecast Visualization
# =========================

st.markdown("---")
st.subheader("📉 Property Price Forecast")

forecast_df = pd.DataFrame({
    "Year": ["Current", "1 Year", "3 Years", "5 Years"],
    "Price": [
        property_data["price"],
        property_data["price_after_1_year"],
        property_data["price_after_3_years"],
        property_data["price_after_5_years"]
    ]
})

fig = px.line(
    forecast_df,
    x="Year",
    y="Price",
    markers=True,
    title="Future Property Price Trend"
)

fig.update_layout(
    xaxis_title="Forecast Period",
    yaxis_title="Property Price (₹)",
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# ROI Analysis
# =========================

st.markdown("---")
st.subheader("💹 Return on Investment (ROI)")

current_price = property_data["price"]
future_price = property_data["price_after_5_years"]

roi = ((future_price - current_price) / current_price) * 100

price_difference = future_price - current_price

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Current Value",
        f"₹ {current_price:,.0f}"
    )

with col2:
    st.metric(
        "5-Year Value",
        f"₹ {future_price:,.0f}"
    )

with col3:
    st.metric(
        "ROI",
        f"{roi:.2f}%"
    )

st.metric(
    "Estimated Profit",
    f"₹ {price_difference:,.0f}"
)
# =========================
# AI Investment Recommendation
# =========================

st.markdown("---")
st.subheader("🤖 AI Investment Recommendation")

growth_score = property_data["growth_score"]
annual_growth = property_data["annual_growth_rate"]

if growth_score >= 8 and annual_growth >= 8:
    recommendation = "🟢 BUY"
    message = """
This property has strong future appreciation potential.

It demonstrates a high growth score and an attractive annual growth rate,
making it suitable for long-term investment.
"""
    risk = "🟢 Low Risk"

elif growth_score >= 5:
    recommendation = "🟡 HOLD"
    message = """
This property has moderate growth potential.

It may generate good returns over time, but market conditions should be
monitored before making additional investments.
"""
    risk = "🟡 Medium Risk"

else:
    recommendation = "🔴 AVOID"
    message = """
The projected appreciation is relatively low.

This property may not provide the expected long-term return compared to
other investment opportunities.
"""
    risk = "🔴 High Risk"

st.success(f"### Recommendation: {recommendation}")

st.info(message)

st.write(f"### Investment Risk Level: {risk}")

# =========================
# Forecast Summary
# =========================

st.markdown("---")
st.subheader("📋 Forecast Summary")

summary = pd.DataFrame({
    "Metric": [
        "Current Price",
        "Price After 1 Year",
        "Price After 3 Years",
        "Price After 5 Years",
        "Annual Growth Rate (%)",
        "Growth Score",
        "ROI (%)",
        "Recommendation"
    ],
    "Value": [
        property_data["price"],
        property_data["price_after_1_year"],
        property_data["price_after_3_years"],
        property_data["price_after_5_years"],
        round(property_data["annual_growth_rate"], 2),
        round(property_data["growth_score"], 2),
        round(roi, 2),
        recommendation
    ]
})

st.dataframe(
    summary,
    use_container_width=True
)

# =========================
# Download Report
# =========================

csv = summary.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Forecast Report",
    data=csv,
    file_name=f"forecast_report_{property_id}.csv",
    mime="text/csv"
)

# =========================
# Footer
# =========================

st.markdown("---")

st.caption(
    "AI-Powered Real Estate Intelligence, Valuation & Investment Recommendation Platform"
)