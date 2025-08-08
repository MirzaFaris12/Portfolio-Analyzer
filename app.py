import streamlit as st
import pandas as pd
import io
import plotly.express as px
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

# --- Session State ---
if "sim_active" not in st.session_state:
    st.session_state.sim_active = False

# 📘 Guide
with st.expander("📘 How to Use This App", expanded=False):
    st.markdown("""
    ### ✅ Upload CSV or Input Tickers
    - Upload your portfolio as CSV (`Ticker`, `Shares`)
    - Or use the P&L Forecaster to test without a file

    ### 🔍 Features:
    - 📊 Allocation and portfolio table
    - 📈 Rebalancing suggestions
    - 📉 Risk analysis (volatility, correlation, Sharpe)
    - 🧠 Risk-based improvement suggestions
    - 🧪 Scenario simulation with reset
    - 💹 P&L forecast with custom change and shares
    """)

# 📁 Upload CSV
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
    try:
        target_dict = {item.split(":")[0].strip(): float(item.split(":")[1]) for item in target_allocation.split(",")}
        rebalance_df = rebalance_portfolio(combined_df, target_dict, total_value)
        st.dataframe(rebalance_df)
    except:
        st.warning("⚠️ Invalid format. Use AAPL:40, MSFT:60")

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

    st.subheader("🧠 Portfolio Improvement Suggestions (Risk-Based)")
    suggestions = suggest_add_remove(combined_df, volatility, vol_rank, sharpe, avg_corr)

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

    # --- Scenario Simulation ---
    st.subheader("🧪 Scenario Simulation")
    with st.form("scenario_sim"):
        sim_ticker = st.text_input("Ticker (e.g., TSLA)")
        sim_action = st.selectbox("Action", ["Add", "Remove"])
        sim_shares = st.number_input("Number of Shares", min_value=1, step=1)
        sim_submit = st.form_submit_button("Run Simulation")

    if st.session_state.sim_active:
        if st.button("🔄 Reset Simulation"):
            st.session_state.sim_active = False
            st.experimental_rerun()

    sim_df = combined_df.copy()

    if sim_submit and sim_ticker:
        sim_ticker = sim_ticker.upper()
        st.session_state.sim_active = True

        if sim_ticker in sim_df["Ticker"].values:
            idx = sim_df[sim_df["Ticker"] == sim_ticker].index[0]
            if sim_action == "Add":
                sim_df.at[idx, "Shares"] += sim_shares
            elif sim_action == "Remove":
                sim_df.at[idx, "Shares"] = max(0, sim_df.at[idx, "Shares"] - sim_shares)
        else:
            if sim_action == "Add":
                sim_data = fetch_market_data([sim_ticker])
                if not sim_data.empty and sim_data["Price"].iloc[0] > 0:
                    new_row = {
                        "Ticker": sim_ticker,
                        "Shares": sim_shares,
                        "Price": sim_data["Price"].iloc[0],
                        "Sector": sim_data["Sector"].iloc[0]
                    }
                    sim_df = pd.concat([sim_df, pd.DataFrame([new_row])], ignore_index=True)
                else:
                    st.error("❌ Invalid or unsupported ticker.")
                    sim_df = None
            else:
                st.warning("⚠️ Ticker not in portfolio.")
                sim_df = None

    if st.session_state.sim_active and sim_df is not None:
        sim_df["Market Value"] = sim_df["Shares"] * sim_df["Price"]
        new_total = sim_df["Market Value"].sum()
        sim_df["Allocation %"] = 100 * sim_df["Market Value"] / new_total

        st.markdown("### 🔁 Simulated Portfolio")
        st.dataframe(sim_df)

        sim_returns = get_daily_returns(sim_df["Ticker"].tolist())
        sim_vol = calculate_volatility(sim_returns)
        sim_sharpe = calculate_sharpe_ratio(sim_returns)
        sim_corr = calculate_correlation_matrix(sim_returns)
        sim_avg_corr = calculate_avg_correlations(sim_corr)
        sim_vol_rank = rank_volatility(sim_vol)

        st.markdown("### 📉 Simulated Risk Metrics")
        st.dataframe(pd.DataFrame({
            "Volatility": sim_vol,
            "Sharpe": sim_sharpe,
            "Avg Correlation": sim_avg_corr,
            "Vol Rank": sim_vol_rank
        }))

        sim_suggestions = suggest_add_remove(sim_df, sim_vol, sim_vol_rank, sim_sharpe, sim_avg_corr)

        st.markdown("### 🧠 Simulated Improvement Suggestions")
        if sim_suggestions["add"]:
            st.markdown("#### ➕ Additions")
            for msg in sim_suggestions["add"]:
                st.write("🔹", msg)
        else:
            st.success("✅ No new sector gaps.")
        if sim_suggestions["remove"]:
            st.markdown("#### ➖ Reductions")
            for msg in sim_suggestions["remove"]:
                st.write("⚠️", msg)
        else:
            st.success("✅ No risky holdings detected.")

# 📉 Quick Profit/Loss Forecast (No CSV Required)
st.subheader("📉 Quick Profit/Loss Forecast (No CSV Needed)")

forecast_raw = st.text_area(
    "Enter expected % change and optional shares per ticker (e.g., AAPL:10:20, TSLA:-5:15)",
    placeholder="TICKER:CHANGE[:SHARES]",
)

if forecast_raw:
    try:
        forecast_data = {}
        for item in forecast_raw.split(","):
            parts = item.strip().split(":")
            ticker = parts[0].upper()
            change = float(parts[1])
            shares = int(parts[2]) if len(parts) > 2 else 10
            forecast_data[ticker] = (change, shares)

        tickers = list(forecast_data.keys())
        market_data = fetch_market_data(tickers)

        if market_data.empty:
            st.error("❌ Could not fetch market data.")
        else:
            df = market_data.copy()
            df["Expected Change (%)"] = df["Ticker"].map(lambda t: forecast_data[t][0])
            df["Shares"] = df["Ticker"].map(lambda t: forecast_data[t][1])
            df["Predicted Price"] = df["Price"] * (1 + df["Expected Change (%)"] / 100)
            df["Current Value"] = df["Price"] * df["Shares"]
            df["Predicted Value"] = df["Predicted Price"] * df["Shares"]
            df["P&L ($)"] = df["Predicted Value"] - df["Current Value"]
            df["P&L (%)"] = (df["P&L ($)"] / df["Current Value"]) * 100

            total_current = df["Current Value"].sum()
            total_predicted = df["Predicted Value"].sum()
            total_gain = total_predicted - total_current
            total_pct = (total_gain / total_current) * 100

            st.markdown("### 📊 Forecast Table")
            st.dataframe(df[[
                "Ticker", "Shares", "Price", "Expected Change (%)", "Predicted Price",
                "Current Value", "Predicted Value", "P&L ($)", "P&L (%)"
            ]])

            st.markdown("### 📉 Forecast Chart")
            chart = px.bar(
                df,
                x="Ticker",
                y="P&L ($)",
                color="P&L ($)",
                color_continuous_scale=["red", "gray", "green"],
                title="Predicted Profit or Loss per Stock"
            )
            st.plotly_chart(chart, use_container_width=True)

            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download Forecast CSV",
                data=csv,
                file_name="pnl_forecast.csv",
                mime="text/csv"
            )

            st.markdown(f"""
            ### 📈 Total Forecast
            - **Total Current Value**: ${total_current:,.2f}  
            - **Predicted Value**: ${total_predicted:,.2f}  
            - **Estimated P&L**: ${total_gain:,.2f} ({total_pct:.2f}%)
            """)

    except Exception as e:
        st.error("⚠️ Invalid input format. Use `TICKER:CHANGE[:SHARES]` (e.g., AAPL:10, TSLA:-5:15)")
        st.exception(e)




