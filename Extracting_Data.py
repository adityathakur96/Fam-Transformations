import pandas as pd

def extract_data(source: str):
    df = pd.read_csv(source)

    required_columns = {
        "date", "open", "high", "low",
        "close", "volume", "ticker"
    }

    # Schema validation by looking on required_columns 
    
    if not required_columns.issubset(df.columns):
        raise ValueError("This is not a valid Schema")
    
    # Generally date in csv file are in format of string so converting them to correct date format

    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"])
    
    df = df.sort_values(["ticker", "date"])
    return df
