import pandas as pd

# Converting of dates to monthly insights

def transform_to_monthly(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.set_index("date")
          .resample("ME")
          .agg(
              open=("open", "first"),
              high=("high", "max"),
              low=("low", "min"),
              close=("close", "last"),
          )
          .reset_index()
    )

# Putting SMA (Simple Moving Average) and EMA (Exponential Moving Average)

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df["sma_10"] = df["close"].rolling(10).mean()
    df["sma_20"] = df["close"].rolling(20).mean()
    df["ema_10"] = df["close"].ewm(span=10, adjust=False).mean()
    df["ema_20"] = df["close"].ewm(span=20, adjust=False).mean()
    return df

# Partioning of main data into 10 different csv files with 24 columns representing 24 months

def transform_per_ticker(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    tdf = df[df["ticker"] == ticker]
    monthly = transform_to_monthly(tdf)
    monthly = add_technical_indicators(monthly)
    return monthly.tail(24)
