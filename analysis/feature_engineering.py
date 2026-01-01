import sqlite3
import pandas as pd
import os

DB_PATH = "database/weather.db"
OUTPUT_PATH = "outputs/engineered_daily_features.csv"

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
"""

df = pd.read_sql_query(query, conn)
conn.close()

if df.empty:
    raise ValueError("No data found in weather_daily_summary")

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["city", "date"])

print("✅ Daily summary data loaded")
print(df.head())
# --------------------------------------------------
# Temperature delta (day-over-day change)
# --------------------------------------------------
df["temp_delta_1d"] = df.groupby("city")["avg_temperature"].diff()

print("✅ Temperature delta feature created")
# --------------------------------------------------
# Rolling averages
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
# Lag features
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
# Temperature volatility (7-day window)
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
os.makedirs("outputs", exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print(f"📁 Engineered features saved to {OUTPUT_PATH}")
