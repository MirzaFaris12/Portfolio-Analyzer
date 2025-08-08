import pandas as pd

def clean_uploaded_file(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    df["Ticker"] = df["Ticker"].str.upper()
    return df
