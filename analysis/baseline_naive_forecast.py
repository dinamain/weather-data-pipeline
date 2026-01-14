"""1️⃣ What this file does (in plain English)

This script answers one core forecasting question:

“If I predict tomorrow’s temperature as today’s temperature, how wrong am I?”

That is the naive baseline."""
import pandas as pd

# ---------------------------------------
# STEP 1: Load the engineered daily data
# ---------------------------------------
df = pd.read_csv("outputs/engineered_daily_features.csv")

print("✅ Data loaded")
print(df[["city", "date", "avg_temperature"]])

# ---------------------------------------
# STEP 2: Convert date and sort properly
# ---------------------------------------
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by=["city", "date"])

# ---------------------------------------
# STEP 3: Naive forecast
# Forecast = yesterday's temperature
# ---------------------------------------
df["naive_forecast"] = (
    df.groupby("city")["avg_temperature"].shift(1)
)

# ---------------------------------------
# STEP 4: Absolute error calculation
# ---------------------------------------
df["naive_error"] = (
    df["avg_temperature"] - df["naive_forecast"]
).abs()

print("\n📊 Naive Forecast Results (Row-level)")
print(
    df[
        [
            "city",
            "date",
            "avg_temperature",
            "naive_forecast",
            "naive_error",
        ]
    ]
)

# ---------------------------------------
# STEP 5: Remove rows where forecast is not possible
# (first day per city)
# ---------------------------------------
valid = df.dropna(subset=["naive_forecast"])

# ---------------------------------------
# STEP 6: Mean Absolute Error per city
# ---------------------------------------
print("\n📉 Mean Absolute Error (Naive Forecast)")
mae = valid.groupby("city")["naive_error"].mean()
print(mae)
