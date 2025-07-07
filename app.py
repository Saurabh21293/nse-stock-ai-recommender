import streamlit as st
import pandas as pd
from recommendation_bot import get_recommendations

st.set_page_config(page_title="NSE Stock AI Recommender", layout="wide")
st.title("📈 NSE Stock Buy/Sell Recommender")

st.markdown("This tool scans the top NSE 200 stocks using RSI and MACD technical indicators and gives buy/sell suggestions with a brief reason.")

with st.spinner("Scanning top stocks..."):
    df = get_recommendations()

if df.empty:
    st.success("✅ No actionable signals today.")
else:
    st.dataframe(df, use_container_width=True)
