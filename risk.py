import yfinance as yf
import pandas as pd
import numpy as np

def get_daily_returns(tickers, period="6mo"):
    data = yf.download(tickers, period=period, interval="1d", group_by='ticker', auto_adjust=True, progress=False)

    if isinstance(tickers, str) or len(tickers) == 1:
        ticker = tickers[0] if isinstance(tickers, list) else tickers
        prices = data["Close"].to_frame(name=ticker)
    else:
        prices = pd.concat([data[ticker]["Close"].rename(ticker) for ticker in tickers], axis=1)

    daily_returns = prices.pct_change().dropna()
    return daily_returns

def calculate_volatility(daily_returns):
    return daily_returns.std() * np.sqrt(252)

def calculate_correlation_matrix(daily_returns):
    return daily_returns.corr()

def calculate_sharpe_ratio(daily_returns, risk_free_rate=0.02):
    # Convert risk-free rate to daily
    daily_rf = (1 + risk_free_rate) ** (1/252) - 1
    excess_returns = daily_returns - daily_rf
    mean_excess = excess_returns.mean()
    volatility = daily_returns.std()
    sharpe_ratio = (mean_excess / volatility) * np.sqrt(252)
    return sharpe_ratio

def calculate_avg_correlations(corr_matrix):
    return corr_matrix.apply(lambda row: row.drop(row.name).mean(), axis=1)

def rank_volatility(volatility_series):
    ranked = volatility_series.rank(pct=True)
    return ranked
