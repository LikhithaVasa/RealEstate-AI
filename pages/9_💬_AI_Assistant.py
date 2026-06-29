import streamlit as st
import pandas as pd

# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="AI Assistant",
    page_icon="💬",
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

st.title("💬 AI Real Estate Assistant")

st.markdown("""
Ask questions about the real estate market, property prices,
investment opportunities, and future forecasts.
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
# Chat History
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# Chat Input
# =========================

question = st.chat_input(
    "Ask anything about the Real Estate Market..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    q = question.lower().strip()

    # =========================
    # AI Response Engine
    # =========================

    if "average price" in q:

        avg_price = df["price"].mean()

        response = (
            f"🏠 The average property price is "
            f"₹ {avg_price:,.0f}."
        )

    elif "highest price" in q:

        highest = df.loc[df["price"].idxmax()]

        response = (
            f"💰 Property ID **{highest['id']}** has the highest price.\n\n"
            f"Current Price: ₹ {highest['price']:,.0f}"
        )

    elif "highest future price" in q:

        highest = df.loc[df["price_after_5_years"].idxmax()]

        response = (
            f"📈 Property ID **{highest['id']}** has the highest "
            f"predicted 5-year value.\n\n"
            f"Future Price: ₹ {highest['price_after_5_years']:,.0f}"
        )

    elif "growth rate" in q:

        growth = df["annual_growth_rate"].mean()

        response = (
            f"📊 Average Annual Growth Rate: "
            f"**{growth:.2f}%**"
        )

    elif "growth score" in q:

        score = df["growth_score"].mean()

        response = (
            f"⭐ Average Growth Score: "
            f"**{score:.2f}**"
        )

    elif "3 bedroom" in q or "3 bhk" in q:

        count = len(
            df[df["number_of_bedrooms"] == 3]
        )

        response = (
            f"🏡 There are **{count}** "
            f"3-bedroom properties in the dataset."
        )

    elif "best postal code" in q:

        postal = (
            df.groupby("postal_code")["price"]
            .mean()
            .idxmax()
        )

        response = (
            f"📍 Postal Code **{postal}** has the "
            f"highest average property price."
        )

    elif "total properties" in q:

        response = (
            f"🏘️ The dataset contains "
            f"**{len(df)}** properties."
        )

    elif "market" in q:

        avg_growth = df["annual_growth_rate"].mean()

        response = (
            f"""
### 📈 Market Overview

• Total Properties: **{len(df)}**

• Average Price: **₹ {df['price'].mean():,.0f}**

• Average Annual Growth Rate: **{avg_growth:.2f}%**

The market shows healthy long-term appreciation
and provides promising investment opportunities.
"""
        )

    elif "investment" in q:

        top = df.loc[df["growth_score"].idxmax()]

        response = (
            f"""
### 🤖 Investment Advice

The best investment opportunity currently is:

**Property ID:** {top['id']}

⭐ Growth Score: {top['growth_score']:.2f}

📈 Annual Growth Rate:
{top['annual_growth_rate']:.2f}%

💰 Current Price:
₹ {top['price']:,.0f}

This property has one of the strongest
future appreciation potentials in the dataset.
"""
        )

    elif "help" in q:

        response = """
You can ask questions like:

• Average price

• Highest price

• Highest future price

• Growth rate

• Growth score

• Best postal code

• Total properties

• 3 bedroom properties

• Market overview

• Investment recommendation
"""

    else:

        response = """
❓ I couldn't understand your question.

Try asking:

• Average price

• Highest price

• Highest future price

• Growth rate

• Growth score

• Best postal code

• Total properties

• 3 bedroom properties

• Market overview

• Investment recommendation

• Help
"""

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )