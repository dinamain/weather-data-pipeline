"""This script is the bridge between raw data and modeling.

It:

Reads daily aggregated weather data from the database

Creates time-series features

Outputs a single canonical ML-ready dataset

👉 Everything downstream (EDA, baselines, ML) depends on this CSV."""

import sqlite3
import pandas as pd
import os

# --------------------------------------------------
# Configuration
# --------------------------------------------------
DB_PATH = "database/weather.db"
OUTPUT_DIR = "outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "engineered_daily_features.csv")

# --------------------------------------------------
# Load daily summary data
# --------------------------------------------------
conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    city,
    date,
    avg_temperature,
    min_temperature,
    max_temperature,
    avg_humidity
FROM weather_daily_summary
ORDER BY city, date
"""

df = pd.read_sql_query(query, conn)
conn.close()

if df.empty:
    raise ValueError("❌ No data found in weather_daily_summary table")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

print("✅ Daily summary data loaded")
print(df.head())

# --------------------------------------------------
# Temperature change (day-over-day)
# --------------------------------------------------
df["temp_delta_1d"] = df.groupby("city")["avg_temperature"].diff()

print("✅ Temperature delta feature created")

# --------------------------------------------------
# Rolling averages (trend smoothing)
# --------------------------------------------------
df["temp_rolling_7d"] = (
    df.groupby("city")["avg_temperature"]
    .rolling(window=7)
    .mean()
    .reset_index(level=0, drop=True)
)

df["temp_rolling_14d"] = (
    df.groupby("city")["avg_temperature"]
    .rolling(window=14)
    .mean()
    .reset_index(level=0, drop=True)
)

print("✅ Rolling average features created")

# --------------------------------------------------
# Lag features (memory)
# --------------------------------------------------
df["temp_lag_1d"] = df.groupby("city")["avg_temperature"].shift(1)
df["temp_lag_7d"] = df.groupby("city")["avg_temperature"].shift(7)

print("✅ Lag features created")

# --------------------------------------------------
# Humidity trend features
# --------------------------------------------------
df["humidity_delta_1d"] = df.groupby("city")["avg_humidity"].diff()

df["humidity_rolling_7d"] = (
    df.groupby("city")["avg_humidity"]
    .rolling(window=7)
    .mean()
    .reset_index(level=0, drop=True)
)

print("✅ Humidity trend features created")

# --------------------------------------------------
# Temperature volatility (stability indicator)
# --------------------------------------------------
df["temp_volatility_7d"] = (
    df.groupby("city")["avg_temperature"]
    .rolling(window=7)
    .std()
    .reset_index(level=0, drop=True)
)

print("✅ Temperature volatility feature created")

# --------------------------------------------------
# Save engineered dataset
# --------------------------------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print(f"📁 Engineered daily features saved to {OUTPUT_FILE}")
