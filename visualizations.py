import plotly.express as px

def plot_allocation_pie(df):
    return px.pie(df, names="Ticker", values="Market Value", title="Asset Allocation")

