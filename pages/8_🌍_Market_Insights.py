import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="Market Insights",
    page_icon="📈",
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

st.title("📈 Market Insights")

st.markdown("""
Explore overall real estate market trends and investment insights.
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
# Market KPIs
# =========================

st.subheader("📊 Market Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Price",
        f"₹ {df['price'].mean():,.0f}"
    )

with col2:
    st.metric(
        "Highest Price",
        f"₹ {df['price'].max():,.0f}"
    )

with col3:
    st.metric(
        "Average Growth",
        f"{df['annual_growth_rate'].mean():.2f}%"
    )

with col4:
    st.metric(
        "Total Properties",
        len(df)
    )

# =========================
# Price Distribution
# =========================

st.subheader("💰 Property Price Distribution")

fig = px.histogram(
    df,
    x="price",
    nbins=40,
    title="Distribution of Property Prices"
)

fig.update_layout(template="plotly_dark")

st.plotly_chart(
    fig,
    use_container_width=True
)
# =========================
# Average Price by Bedrooms
# =========================

st.markdown("---")
st.subheader("🛏️ Average Price by Number of Bedrooms")

bedroom_price = (
    df.groupby("number_of_bedrooms")["price"]
      .mean()
      .reset_index()
)

fig = px.bar(
    bedroom_price,
    x="number_of_bedrooms",
    y="price",
    title="Average Property Price by Bedrooms",
    text_auto=".2s"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Bedrooms",
    yaxis_title="Average Price"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# Top Postal Codes
# =========================

st.markdown("---")
st.subheader("📍 Top 10 Postal Codes by Average Price")

postal_price = (
    df.groupby("postal_code")["price"]
      .mean()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig = px.bar(
    postal_price,
    x="postal_code",
    y="price",
    title="Top 10 Postal Codes",
    text_auto=".2s"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Postal Code",
    yaxis_title="Average Price"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# Property Age Distribution
# =========================

st.markdown("---")
st.subheader("🏡 Property Age Distribution")

fig = px.histogram(
    df,
    x="property_age",
    nbins=30,
    title="Distribution of Property Age"
)

fig.update_layout(template="plotly_dark")

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# Growth Score Analysis
# =========================

st.markdown("---")
st.subheader("📈 Growth Score Distribution")

fig = px.histogram(
    df,
    x="growth_score",
    nbins=25,
    title="Growth Score Distribution"
)

fig.update_layout(template="plotly_dark")

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# AI Market Summary
# =========================

st.markdown("---")
st.subheader("🤖 AI Market Insights")

avg_growth = df["annual_growth_rate"].mean()
avg_price = df["price"].mean()

highest_postal = postal_price.iloc[0]["postal_code"]

st.success(
    f"""
### Market Summary

• Average Property Price: ₹ {avg_price:,.0f}

• Average Annual Growth Rate: {avg_growth:.2f}%

• Highest Performing Postal Code: {highest_postal}

• The market shows steady appreciation and offers
good opportunities for long-term investment,
especially in high-growth locations.
"""
)

st.info(
"""
The dashboard combines historical property information,
forecasting results and growth metrics to help users
understand market trends and identify promising
investment opportunities.
"""
)
