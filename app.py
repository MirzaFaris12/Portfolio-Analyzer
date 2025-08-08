import streamlit as st
import pandas as pd
from data import fetch_market_data
from portfolio import compute_portfolio_metrics, rebalance_portfolio
from visualizations import plot_allocation_pie
from utils import clean_uploaded_file
from risk import (
    get_daily_returns,
    calculate_volatility,
    calculate_correlation_matrix,
    calculate_sharpe_ratio,
    calculate_avg_correlations,
    rank_volatility
)
from advisor import suggest_add_remove

st.set_page_config(page_title="💼 Portfolio Health Analyzer", layout="wide")
st.title("💼 Portfolio Health Analyzer")

# 📘 App Guide
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
       Enter your target allocation (e.g., `AAPL:40, MSFT:60`) and the app shows how much to buy/sell to reach that goal.

    5. **Risk Analysis**  
       - 📉 Volatility: How risky each stock is  
       - ⚖️ Sharpe Ratio: Return per unit of risk  
       - 🔗 Correlation Matrix: How your assets move together

    6. **Improvement Suggestions**  
       - ❌ Flags stocks that are too volatile, too correlated, or underperforming  
       - ➕ Recommends adding ETFs from sectors you’re missing
    """)

# 📁 File Upload
uploaded_file = st.file_uploader("Upload Portfolio CSV (Ticker, Shares)", type="csv")

if uploaded_file:
    df = clean_uploaded_file(uploaded_file)
    market_df = fetch_market_data(df['Ticker'].tolist())
    combined_df, total_value = compute_portfolio_metrics(df, market_df)

    # 📊 Allocation Pie Chart
    st.subheader("📊 Portfolio Allocation")
    st.plotly_chart(plot_allocation_pie(combined_df), use_container_width=True)

    # 📋 Portfolio Table
    st.subheader("📋 Portfolio Overview")
    st.dataframe(combined_df)

    # 📈 Rebalancing Tool
    st.subheader("📈 Rebalancing Suggestions")
    target_allocation = st.text_area("Enter Target Allocation % (e.g., AAPL:40, MSFT:60)", value="AAPL:50, MSFT:50")
    try:
        target_dict = {item.split(":")[0].strip(): float(item.split(":")[1]) for item in target_allocation.split(",")}
        rebalance_df = rebalance_portfolio(combined_df, target_dict, total_value)
        st.dataframe(rebalance_df)
    except:
        st.warning("⚠️ Please enter a valid allocation format (e.g., AAPL:40, MSFT:60)")

    # 📉 Risk Analysis Section
    st.subheader("📉 Risk Analysis")

    daily_returns = get_daily_returns(df['Ticker'].tolist())
    volatility = calculate_volatility(daily_returns)
    sharpe = calculate_sharpe_ratio(daily_returns)
    corr_matrix = calculate_correlation_matrix(daily_returns)
    avg_corr = calculate_avg_correlations(corr_matrix)
    vol_rank = rank_volatility(volatility)

    st.markdown("**📌 Annualized Volatility**")
    st.dataframe(volatility.rename("Volatility (σ)").to_frame())

    st.markdown("**📌 Sharpe Ratio**")
    st.dataframe(sharpe.rename("Sharpe Ratio").to_frame())

    st.markdown("**📌 Asset Correlation Matrix**")
    try:
        st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm', axis=None))
    except:
        st.dataframe(corr_matrix)

    # 🧠 Risk-Based Add/Remove Suggestions
    st.subheader("🧠 Portfolio Improvement Suggestions (Risk-Based)")

    suggestions = suggest_add_remove(
        combined_df, volatility, vol_rank, sharpe, avg_corr
    )

    if suggestions["add"]:
        st.markdown("### ➕ Suggested Additions")
        for msg in suggestions["add"]:
            st.write("🔹", msg)
    else:
        st.success("✅ No missing sector exposures detected.")

    if suggestions["remove"]:
        st.markdown("### ➖ Suggested Reductions")
        for msg in suggestions["remove"]:
            st.write("⚠️", msg)
    else:
        st.success("✅ No risky holdings flagged for removal.")
else:
    st.info("📁 Upload a CSV file with columns: Ticker, Shares")


