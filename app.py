import streamlit as st
import pandas as pd
from data import fetch_market_data
from portfolio import compute_portfolio_metrics, rebalance_portfolio
from visualizations import plot_allocation_pie
from utils import clean_uploaded_file

st.set_page_config(page_title="💼 Portfolio Health Analyzer", layout="wide")
st.title("💼 Portfolio Health Analyzer")

uploaded_file = st.file_uploader("Upload Portfolio CSV (Ticker, Shares)", type="csv")

if uploaded_file:
    df = clean_uploaded_file(uploaded_file)
    market_df = fetch_market_data(df['Ticker'].tolist())
    combined_df, total_value = compute_portfolio_metrics(df, market_df)

    st.subheader("📊 Portfolio Allocation")
    st.plotly_chart(plot_allocation_pie(combined_df), use_container_width=True)

    st.subheader("📋 Portfolio Overview")
    st.dataframe(combined_df)

    st.subheader("📈 Rebalancing Suggestions")
    target_allocation = st.text_area("Enter Target Allocation % (e.g., AAPL:40, MSFT:60)", value="AAPL:50, MSFT:50")
    target_dict = {item.split(":")[0].strip(): float(item.split(":")[1]) for item in target_allocation.split(",")}
    rebalance_df = rebalance_portfolio(combined_df, target_dict, total_value)
    st.dataframe(rebalance_df)
else:
    st.info("Upload a CSV to get started.")
