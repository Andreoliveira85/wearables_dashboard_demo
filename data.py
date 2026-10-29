"""
data.py
-------
Functions to load and filter the data. No plotting here!
"""

from pathlib import Path

import pandas as pd

from config import DATA_PATH


def load_data(path=DATA_PATH):
    """Read the CSV, parse dates and remove sensor glitches."""
    full_path = Path(__file__).parent / path      # works no matter where you run the app from
    df = pd.read_csv(full_path, parse_dates=["date"])
    df = df[df["steps"] < 50_000]                 # glitches found during the EDA
    return df


def filter_data(df, cities=None, devices=None, start_date=None, end_date=None):
    """Return only the rows that match the filters chosen in the dashboard."""
    if cities:
        df = df[df["city"].isin(cities)]
    if devices:
        df = df[df["device"].isin(devices)]
    if start_date:
        df = df[df["date"] >= start_date]
    if end_date:
        df = df[df["date"] <= end_date]
    return df


if __name__ == "__main__":
    # Quick test: python data.py
    data = load_data()
    print(data.shape)
    print(filter_data(data, cities=["Berlin"], devices=["Garmin"]).head())