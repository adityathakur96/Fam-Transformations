from Extracting_Data import extract_data
from Transforming_Data import transform_per_ticker
from Loading_Data import load_data

# Making all 3 files run by this run_pipeline function 
def run_pipeline(input_path: str):
    tickers = [
        "AAPL","AMD","AMZN","AVGO","CSCO",
        "MSFT","NFLX","PEP","TMUS","TSLA"
    ]

    raw_df = extract_data(input_path)

    for ticker in tickers:
        transformed = transform_per_ticker(raw_df, ticker)
        load_data(transformed, ticker)

if __name__ == "__main__":
    # we can also use the normal csv file instead of using raw github url 
    # Financial_Records.csv is  output_file.csv
    # run_pipeline(Financial_Records.csv) 
    run_pipeline(
    "https://raw.githubusercontent.com/sandeep-tt/tt-intern-dataset/main/output_file.csv"
)   

