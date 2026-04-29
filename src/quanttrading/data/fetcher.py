import yfinance as yf
import pandas as pd


# DOWNLOAD DATA BY YFINANCE
def download_data(ticker, period, interval):
    df = yf.download(ticker=ticker, period=period, interval=interval)
    return df

# ADD RETURN COLUMN
def add_returns(df):
    df['Retun'] = df['Close'].pct_change() * 100
    return df

# MERGE download_data AND add_returns, ALSO CLEAN THE DATA
def prepare_data(ticker, period, interval):
    df = download_data(ticker, period, interval)
    df.columns = df.columns.get_level_values(0)
    df = add_returns(df)
    df = df.dropna()
    return df