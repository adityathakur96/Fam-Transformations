# Fam Transformations — Data Engineering Intern Assignment 📈

**Overview**

This project implements the Data Engineering intern assignment: convert a 2-year daily stock price dataset (10 tickers) into monthly summaries, compute technical indicators (SMA/EMA), and produce one CSV per ticker with 24 monthly rows each.

---

## Problem Statement (as submitted)

- Resample daily data to **monthly** frequency.
- Compute monthly OHLC using:
  - **Open** = price on the first trading day of the month
  - **Close** = price on the last trading day of the month
  - **High** = maximum daily high in the month
  - **Low** = minimum daily low in the month
- Compute technical indicators on monthly `close` prices:
  - **SMA_10, SMA_20** (Simple Moving Average for N = 10 and 20 months)
  - **EMA_10, EMA_20** (Exponential Moving Average for N = 10 and 20 months)
- Partition outputs into 10 files named `result_{SYMBOL}.csv`, each containing **exactly 24 rows**.


## Data Schema (Input)

Input CSV columns: `date,volume,open,high,low,close,adjclose,ticker`.
Tickers: `AAPL, AMD, AMZN, AVGO, CSCO, MSFT, NFLX, PEP, TMUS, TSLA`.

Note: The pipeline accepts either a local file (`Financial_Records.csv`) or a remote URL (this repo uses the raw GitHub CSV by default to simulate a real-world remote data source).
Default remote dataset URL used in `Orchestration.py`:

`https://raw.githubusercontent.com/sandeep-tt/tt-intern-dataset/main/output_file.csv`

---

## Implementation

- Clean, modular Python (pandas) ETL:
  - `Extracting_Data.py` — `extract_data(source: str)`: reads CSV (URL or local), validates columns, converts `date` to datetime, sorts by `ticker, date`.
  - `Transforming_Data.py` —
    - `transform_to_monthly(df)` — resamples at **month-end** (`ME`) and aggregates `open` (first), `high` (max), `low` (min), `close` (last).
    - `add_technical_indicators(df)` — computes `sma_10`, `sma_20`, `ema_10`, `ema_20` using `rolling` and `ewm`.
    - `transform_per_ticker(df, ticker)` — filters ticker, creates monthly summary, adds indicators, returns last 24 months.
  - `Loading_Data.py` — `load_data(df, ticker, output_dir='.')`: writes `Results/result_{TICKER}.csv`.
  - `Orchestration.py` — runner that ties extraction, transformation, and loading for the 10 tickers (uses the raw GitHub CSV by default but accepts a local filename like `Financial_Records.csv`).

- No third-party TA libraries — all indicators computed with pandas vectorized operations (rolling mean and ewm).

---

## How to run (Quick Start)

Requirements:
- Python 3.8+
- pandas

Install:
```bash
pip install pandas
```

Run the pipeline (uses the raw GitHub CSV by default):
```bash
python Orchestration.py
```

Or call the function with a local CSV file (example uses the included `Financial_Records.csv`):
```python
from Orchestration import run_pipeline
run_pipeline("Financial_Records.csv")
```

Outputs are created in `Results/` with filenames like `result_AAPL.csv`.

---

## Validation

- I validated outputs programmatically: the `Results/` folder contains **10 CSV files** (`result_AAPL.csv` … `result_TSLA.csv`) and **each file contains 24 rows** (monthly records for the 2-year period).

---

## Assumptions & Notes

- Using the raw GitHub URL simulates reading from a remote data source (S3, HTTP endpoint); the code accepts URLs or local files.
- Month-end (`ME`) resampling is used to create monthly aggregates; "open" uses first trading day in month and "close" uses last trading day.
- First EMA values are seeded using the corresponding SMA (common practice for stability).
- If a ticker has fewer than 24 months in the input, its output will have fewer rows — tests should assert 24 rows for full 2-year datasets.

---