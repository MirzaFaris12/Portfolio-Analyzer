import yfinance as yf
import pandas as pd
import numpy as np

def get_daily_returns(tickers, period="6mo"):
    data = yf.download(tickers, period=period, interval="1d", group_by='ticker', auto_adjust=True, progress=False)

    if isinstance(tickers, str) or len(tickers) == 1:
        # Handle single ticker
        ticker = tickers[0] if isinstance(tickers, list) else tickers
        prices = data["Close"].to_frame(name=ticker)
    else:
        # Multiple tickers: extract Close price for each
        prices = pd.concat([data[ticker]["Close"].rename(ticker) for ticker in tickers], axis=1)

    daily_returns = prices.pct_change().dropna()
    return daily_returns

def calculate_volatility(daily_returns):
    return daily_returns.std() * np.sqrt(252)

def calculate_correlation_matrix(daily_returns):
    return daily_returns.corr()
