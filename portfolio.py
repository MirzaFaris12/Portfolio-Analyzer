import pandas as pd

def compute_portfolio_metrics(df, market_df):
    df = df.merge(market_df, on="Ticker", how="left")
    df["Market Value"] = df["Shares"] * df["Price"]
    total_value = df["Market Value"].sum()
    df["Allocation %"] = 100 * df["Market Value"] / total_value
    return df, total_value

def rebalance_portfolio(df, target_allocation, total_value):
    df["Target %"] = df["Ticker"].map(target_allocation).fillna(0)
    df["Target Value"] = df["Target %"] * total_value / 100
    df["Rebalance Action ($)"] = df["Target Value"] - df["Market Value"]
    return df[["Ticker", "Shares", "Price", "Market Value", "Allocation %", "Target %", "Target Value", "Rebalance Action ($)"]]
