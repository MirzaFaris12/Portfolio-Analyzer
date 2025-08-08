import yfinance as yf
import pandas as pd
import numpy as np

def get_daily_returns(tickers, period="6mo"):
    price_data = yf.download(tickers, period=period, interval="1d", group_by='ticker', auto_adjust=True, progress=False)
    
    # If only one ticker, ensure consistent format
    if isinstance(price_data.columns, pd.Index):
        price_data = pd.concat([price_data['Close']], axis=1, keys=tickers)
    else:
        price_data = price_data['Close']
    
    daily_returns = price_data.pct_change().dropna()
    return daily_returns

def calculate_volatility(daily_returns):
    return daily_returns.std() * np.sqrt(252)  # Annualized volatility

def calculate_correlation_matrix(daily_returns):
    return daily_returns.corr()
