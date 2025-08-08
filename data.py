import yfinance as yf
import pandas as pd

def fetch_market_data(tickers):
    prices = {}
    sectors = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            prices[ticker] = stock.info['regularMarketPrice']
            sectors[ticker] = stock.info.get("sector", "Unknown")
        except:
            prices[ticker] = 0
            sectors[ticker] = "Unknown"
    return pd.DataFrame({
        "Ticker": tickers,
        "Price": [prices[t] for t in tickers],
        "Sector": [sectors[t] for t in tickers]
    })

