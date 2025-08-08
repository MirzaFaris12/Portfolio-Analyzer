import pandas as pd

SECTOR_ETF_MAP = {
    "Technology": "XLK",
    "Healthcare": "XLV",
    "Financial Services": "XLF",
    "Consumer Defensive": "XLP",
    "Industrials": "XLI",
    "Energy": "XLE",
    "Utilities": "XLU",
    "Communication Services": "XLC",
    "Materials": "XLB",
    "Real Estate": "XLRE"
}

def suggest_add_remove(
    portfolio_df,
    volatility,
    vol_rank,
    sharpe_ratio,
    avg_correlation,
    max_volatility_rank=0.80,
    max_avg_corr=0.9,
    min_sharpe_ratio=0.2
):
    suggestions = {"add": [], "remove": []}

    held_sectors = portfolio_df["Sector"].unique()
    tickers = portfolio_df["Ticker"].tolist()

    # ➕ Suggest ADD based on missing sectors
    for sector, etf in SECTOR_ETF_MAP.items():
        if sector not in held_sectors:
            suggestions["add"].append(f"{sector} exposure missing. Suggest adding {etf}.")

    # ➖ Suggest REMOVE based on risk metrics
    for ticker in tickers:
        reasons = []
        if vol_rank.get(ticker, 0) >= max_volatility_rank:
            reasons.append("high volatility")

        if avg_correlation.get(ticker, 0) >= max_avg_corr:
            reasons.append("strong correlation with other assets")

        if sharpe_ratio.get(ticker, 1) < min_sharpe_ratio:
            reasons.append("low Sharpe ratio")

        if reasons:
            msg = f"{ticker} flagged for: {', '.join(reasons)}. Consider reviewing this position."
            suggestions["remove"].append(msg)

    return suggestions

