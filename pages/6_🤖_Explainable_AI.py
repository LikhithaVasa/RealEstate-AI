import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import os
import shap
import numpy as np

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Explainable AI",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# Load CSS
# =====================================================

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# =====================================================
# Title
# =====================================================

st.title("🧠 Explainable AI Dashboard")

st.markdown("""
Understand how the LightGBM model predicts house prices using
Explainable Artificial Intelligence (XAI).

This dashboard provides both:

- Global Explainability
- Local Explainability
""")

# =====================================================
# Load Model
# =====================================================

@st.cache_resource
def load_model():
    return joblib.load(
        "models/best_house_price_model.pkl"
    )

model = load_model()

# =====================================================
# Feature Importance
# =====================================================

feature_names = model.feature_name_

importance = model.feature_importances_

importance_df = pd.DataFrame({

    "Feature": feature_names,

    "Importance": importance

})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

st.subheader("🏆 Top 10 Important Features")

st.dataframe(
    importance_df.head(10),
    use_container_width=True
)

fig = px.bar(

    importance_df.head(10),

    x="Importance",

    y="Feature",

    orientation="h",

    color="Importance",

    title="Feature Importance Ranking"

)

fig.update_layout(

    template="plotly_dark",

    height=550

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# SHAP Global Explainability
# =====================================================

st.markdown("---")

st.subheader("📊 SHAP Global Explainability")

st.write("""

The SHAP Summary Plot explains how every feature
affects predictions across the entire dataset.

### Interpretation

🔴 Red = High feature value

🔵 Blue = Low feature value

➡ Features near the top have the largest influence
on predicted house prices.

""")

shap_image = "assets/shap_summary.png"

if os.path.exists(shap_image):

    st.image(
        shap_image,
        use_container_width=True
    )

else:

    st.warning(
        "SHAP Summary Plot not found."
    )
# =====================================================
# Local SHAP Explainability
# =====================================================

st.markdown("---")

st.subheader("🔍 Local Explainability")

st.write("""
Select a property to understand **why** the AI predicted
its house price.

The SHAP values show which features increased or
decreased the prediction.
""")

# Load Dataset

df = pd.read_csv(
    "dataset/processed/future_price_forecast.csv"
)

df = df.rename(
    columns={
        "area_of_the_house(excluding_basement)":
        "house_area_without_basement"
    }
)

# Load SHAP Files

shap_values = joblib.load(
    "models/shap_values.pkl"
)

X = joblib.load(
    "models/shap_features.pkl"
)

# Property Selection

property_index = st.selectbox(

    "Select Property",

    options=df.index,

    format_func=lambda x:
    f"Property ID : {df.loc[x,'id']}"

)

# Selected SHAP Values

selected_shap = shap_values[property_index]

selected_data = X.iloc[property_index]

# Create Contribution DataFrame

contribution_df = pd.DataFrame({

    "Feature": X.columns,

    "Contribution": selected_shap

})

contribution_df["Impact"] = contribution_df["Contribution"].abs()

contribution_df = contribution_df.sort_values(

    by="Impact",

    ascending=False

)

# Prediction

prediction = model.predict(
    selected_data.values.reshape(1,-1)
)[0]

actual_price = df.loc[property_index,"price"]

# Metrics

col1,col2 = st.columns(2)

with col1:

    st.metric(

        "Actual Price",

        f"₹ {actual_price:,.0f}"

    )

with col2:

    st.metric(

        "Predicted Price",

        f"₹ {prediction:,.0f}"

    )

st.markdown("---")

st.subheader("📊 Top Feature Contributions")

st.dataframe(

    contribution_df.head(10),

    use_container_width=True

)
# =====================================================
# Positive & Negative Contributions
# =====================================================

positive = contribution_df[
    contribution_df["Contribution"] > 0
].sort_values(
    by="Contribution",
    ascending=False
).head(5)

negative = contribution_df[
    contribution_df["Contribution"] < 0
].sort_values(
    by="Contribution"
).head(5)

col1, col2 = st.columns(2)

with col1:

    st.success("### 🟢 Top Positive Contributors")

    if len(positive) > 0:

        for _, row in positive.iterrows():

            st.write(
                f"✅ **{row['Feature']}** "
                f"(+{row['Contribution']:.2f})"
            )

    else:

        st.info("No positive contributors found.")

with col2:

    st.error("### 🔴 Top Negative Contributors")

    if len(negative) > 0:

        for _, row in negative.iterrows():

            st.write(
                f"❌ **{row['Feature']}** "
                f"({row['Contribution']:.2f})"
            )

    else:

        st.info("No negative contributors found.")

# =====================================================
# Model Summary
# =====================================================

st.markdown("---")

st.subheader("📋 Model Summary")

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Model",
        "LightGBM"
    )

with c2:

    st.metric(
        "Total Features",
        len(feature_names)
    )

with c3:

    st.metric(
        "Top Feature",
        importance_df.iloc[0]["Feature"]
    )

# =====================================================
# AI Explanation
# =====================================================

st.markdown("---")

st.subheader("🤖 AI Interpretation")

st.success(
    f"""
The predicted price is primarily influenced by:

🏆 **{importance_df.iloc[0]['Feature']}**

The model combines multiple factors including
property size, location, house quality,
surrounding infrastructure, and property age
to estimate market value.
"""
)

st.info("""
### How to interpret this page

🟢 Positive Contribution

These features increased the predicted house price.

🔴 Negative Contribution

These features reduced the predicted house price.

📊 SHAP values provide transparency by explaining
how each feature contributes to an individual prediction,
making the AI model more interpretable and trustworthy.
""")
# =====================================================
# Download Reports
# =====================================================

st.markdown("---")

st.subheader("📥 Download Explainability Reports")

csv = contribution_df.to_csv(index=False).encode("utf-8")

col1, col2 = st.columns(2)

with col1:

    st.download_button(
        label="📄 Download Local SHAP Report",
        data=csv,
        file_name="local_shap_report.csv",
        mime="text/csv"
    )

with col2:

    csv2 = importance_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📊 Download Feature Importance",
        data=csv2,
        file_name="feature_importance.csv",
        mime="text/csv"
    )

# =====================================================
# Footer
# =====================================================

st.markdown("---")

st.caption(
    """
    Explainable AI Dashboard • Powered by LightGBM + SHAP

    This dashboard provides both **Global Explainability**
    and **Local Explainability** to improve the transparency
    of AI-based house price prediction.
    """
)