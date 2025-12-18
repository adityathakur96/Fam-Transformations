import pandas as pd

# Puting the results on the same location 

def load_data(df: pd.DataFrame, ticker: str, output_dir: str = "."):
    
    df.to_csv(f"{output_dir}/Results/result_{ticker}.csv", index=False)
