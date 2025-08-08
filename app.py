import streamlit as st
import pandas as pd
from data import fetch_market_data
from portfolio import compute_portfolio_metrics, rebalance_portfolio
from visualizations import plot_allocation_pie
from utils import clean_uploaded_file
from risk import get_daily_returns, calculate_volatility, calculate_correlation_matrix

st.set_page_config(page_title="💼 Portfolio Health Analyzer", layout="wide")
st.title("💼 Portfolio Health Analyzer")

with st.expander("📘 How to Use This App", expanded=False):
    st.markdown("""
    Welcome to the **Portfolio Health Analyzer**! This app helps you understand your investment portfolio and make smarter decisions.

    ### ✅ How to Use:
    1. **Upload CSV File**  
       Upload a `.csv` with two columns: `Ticker` and `Shares` (e.g., AAPL, 10).

    2. **Portfolio Allocation**  
       Visual pie chart showing the % of each asset in your portfolio.

    3. **Portfolio Overview**  
       Table showing live prices, value per stock, and your current allocation.

    4. **Rebalancing Suggestions**  
       Enter your target allocation (e.g., `AAPL:50, MSFT:50`) and the app shows how much to buy/sell to reach that goal.

    5. **Risk Analysis**  
       - 📉 Annualized Volatility: How risky each stock is based on price fluctuations  
       - 🔗 Correlation Matrix: How your assets move together (1 = highly correlated)

    > 💡 Tip: Diversify by reducing high correlations and spreading across sectors.

    ---
    **Sample CSV Format:**
    ```
    Ticker,Shares
    AAPL,10
    MSFT,8
    GOOGL,5
    ```
    """)


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

    st.subheader("📉 Risk Analysis")

    daily_returns = get_daily_returns(df['Ticker'].tolist())
    volatility = calculate_volatility(daily_returns)
    corr_matrix = calculate_correlation_matrix(daily_returns)

    st.markdown("**📌 Annualized Volatility**")
    st.dataframe(volatility.rename("Volatility (σ)").to_frame())

    st.markdown("**📌 Asset Correlation Matrix**")
    st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm', axis=None))

else:
    st.info("📁 Upload a CSV file with columns: Ticker, Shares")

