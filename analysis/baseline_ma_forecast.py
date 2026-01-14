"""1️⃣ What this file does (clearly)

This script implements a 2-day Moving Average (MA-2) forecast:

“Predict today’s temperature as the average of the previous 2 days (no future leakage).”

This is the next logical baseline after naive forecasting."""

import pandas as pd

# ---------------------------------------
# Load daily engineered data
# ---------------------------------------
df = pd.read_csv("outputs/engineered_daily_features.csv")

print("✅ Data loaded")
print(df[["city", "date", "avg_temperature"]])

# ---------------------------------------
# Prepare data
# ---------------------------------------
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by=["city", "date"])

# ---------------------------------------
# Moving Average Forecast (2-day)
# Use past 2 days ONLY
# ---------------------------------------
df["ma_2_forecast"] = (
    df.groupby("city")["avg_temperature"]
      .shift(1)
      .rolling(window=2)
      .mean()
)

# ---------------------------------------
# Compute MA absolute error
# ---------------------------------------
df["ma_2_error"] = (
    df["avg_temperature"] - df["ma_2_forecast"]
).abs()

print("\n📊 Moving Average Forecast Results")
print(
    df[
        [
            "city",
            "date",
            "avg_temperature",
            "ma_2_forecast",
            "ma_2_error"
        ]
    ]
)

# ---------------------------------------
# Drop rows where forecast not possible
# ---------------------------------------
valid = df.dropna(subset=["ma_2_forecast"])

# ---------------------------------------
# MAE per city
# ---------------------------------------
print("\n📉 Mean Absolute Error (MA-2 Forecast)")
mae = valid.groupby("city")["ma_2_error"].mean()
print(mae)
