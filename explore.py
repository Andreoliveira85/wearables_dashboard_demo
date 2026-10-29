"""
explore.py
----------
Your first Python script: load the data and print a quick summary.

Run it from the terminal:
    python explore.py
"""

import pandas as pd

DATA_PATH = "data/wearables_daily.csv"


def summarize(path):
    """Load the CSV and print the basics we always check first."""
    df = pd.read_csv(path, parse_dates=["date"])
    print(f"{len(df):,} rows · {df['user_id'].nunique()} users")
    print(f"From {df['date'].min():%d %b %Y} to {df['date'].max():%d %b %Y}")
    print("\nUsers per device:")
    print(df.drop_duplicates("user_id")["device"].value_counts())
    print("\nAverage daily steps per city:")
    print(df.groupby("city")["steps"].mean().round(0).sort_values(ascending=False))
    return df


if __name__ == "__main__":
    summarize(DATA_PATH)