import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="EDA Dashboard",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------------------
# LOAD CSS
# ----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "assets" / "style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ----------------------------------------------------
# LOAD DATASET
# ----------------------------------------------------

DATA_PATH = (
    BASE_DIR
    / "dataset"
    / "cleaned"
    / "final_engineered_dataset.csv"
)

df = pd.read_csv(DATA_PATH)

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

st.markdown(
"""
<div class="main-title">

📊 Real Estate Analytics Dashboard

</div>

<div class="subtitle">

Exploratory Data Analysis of Real Estate Dataset

</div>
""",
unsafe_allow_html=True
)

st.write("")
st.header("📌 Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Records",
        f"{len(df):,}"
    )

with c2:
    st.metric(
        "Total Features",
        df.shape[1]
    )

with c3:
    st.metric(
        "Missing Values",
        int(df.isna().sum().sum())
    )

with c4:
    st.metric(
        "Duplicate Records",
        int(df.duplicated().sum())
    )

st.divider()
st.header("📋 Dataset Preview")

st.dataframe(
    df.head(10),
    use_container_width=True
)

st.divider()
st.header("📈 Dataset Statistics")

st.dataframe(
    df.describe(),
    use_container_width=True
)

st.divider()
# ----------------------------------------------------
# PRICE DISTRIBUTION
# ----------------------------------------------------

st.header("💰 Property Price Distribution")

fig = px.histogram(
    df,
    x="price",
    nbins=50,
    title="Distribution of Property Prices"
)

fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# ----------------------------------------------------
# LIVING AREA
# ----------------------------------------------------

st.header("🏠 Living Area Distribution")

fig = px.histogram(
    df,
    x="living_area",
    nbins=40,
    title="Living Area Distribution"
)

fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# ----------------------------------------------------
# BEDROOMS
# ----------------------------------------------------

st.header("🛏 Bedrooms Distribution")

bedroom_counts = (
    df["number_of_bedrooms"]
    .value_counts()
    .sort_index()
)

fig = px.bar(
    x=bedroom_counts.index,
    y=bedroom_counts.values,
    labels={
        "x":"Bedrooms",
        "y":"Count"
    },
    title="Number of Bedrooms"
)

fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# ----------------------------------------------------
# BATHROOMS
# ----------------------------------------------------

st.header("🚿 Bathrooms Distribution")

bath_counts = (
    df["number_of_bathrooms"]
    .value_counts()
    .sort_index()
)

fig = px.bar(
    x=bath_counts.index,
    y=bath_counts.values,
    labels={
        "x":"Bathrooms",
        "y":"Count"
    },
    title="Bathrooms Distribution"
)

fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# ----------------------------------------------------
# PRICE OUTLIERS
# ----------------------------------------------------

st.header("📦 Price Outlier Detection")

fig = px.box(
    df,
    y="price",
    title="Property Price Outliers"
)

fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# ----------------------------------------------------
# AREA OUTLIERS
# ----------------------------------------------------

st.header("📐 Living Area Outliers")

fig = px.box(
    df,
    y="living_area",
    title="Living Area Outliers"
)

fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# ----------------------------------------------------
# CORRELATION HEATMAP
# ----------------------------------------------------

st.header("🔥 Feature Correlation Heatmap")

corr = df.corr(numeric_only=True)

fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    aspect="auto",
    title="Correlation Matrix"
)

fig.update_layout(
    template="plotly_dark",
    height=850
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# ----------------------------------------------------
# SCATTER PLOT
# ----------------------------------------------------

st.header("📉 Living Area vs Property Price")

fig = px.scatter(

    df,

    x="living_area",

    y="price",

    color="number_of_bedrooms",

    hover_data=[
    "number_of_bathrooms"
    ],

    title="Living Area vs Price"

)

fig.update_layout(

    template="plotly_dark",

    height=600

)

st.plotly_chart(

    fig,

    use_container_width=True

)
# ----------------------------------------------------
# TOP CORRELATIONS
# ----------------------------------------------------

st.header("🏆 Top Features Correlated with Price")

price_corr = (

    corr["price"]

    .drop("price")

    .abs()

    .sort_values(
        ascending=False
    )

)

top10 = price_corr.head(10)

fig = px.bar(

    x=top10.values,

    y=top10.index,

    orientation="h",

    labels={
        "x":"Correlation",
        "y":"Feature"
    },

    title="Top Features Affecting Price"

)

fig.update_layout(

    template="plotly_dark",

    height=600

)

st.plotly_chart(

    fig,

    use_container_width=True

)
# ----------------------------------------------------
# INTERACTIVE ANALYSIS
# ----------------------------------------------------

st.header("🎛 Interactive Feature Explorer")

numeric_cols = df.select_dtypes(
    include="number"
).columns.tolist()

x_feature = st.selectbox(

    "Select X-Axis",

    numeric_cols,

    index=numeric_cols.index("living_area")

)

y_feature = st.selectbox(

    "Select Y-Axis",

    numeric_cols,

    index=numeric_cols.index("price")

)

fig = px.scatter(

    df,

    x=x_feature,

    y=y_feature,

    color="number_of_bedrooms",

    title=f"{x_feature} vs {y_feature}"

)

fig.update_layout(

    template="plotly_dark",

    height=650

)

st.plotly_chart(

    fig,

    use_container_width=True

)
# ----------------------------------------------------
# CORRELATION TABLE
# ----------------------------------------------------

st.header("📋 Complete Correlation Matrix")

st.dataframe(

    corr,

    use_container_width=True,

    height=500

)
st.divider()

st.success(
    "EDA Dashboard Completed Successfully!"
)

st.caption(
    "AI Powered Real Estate Intelligence Platform | Exploratory Data Analysis Dashboard"
)