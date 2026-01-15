"""
MA(5) Time-Series Forecast

What this file does:
- Uses past 5 days to forecast the next day
- Respects time order (no leakage)
- Evaluates on last day per city
"""

import pandas as pd

# --------------------------------------------------
# STEP 1: Load engineered daily data
# --------------------------------------------------
df = pd.read_csv("outputs/engineered_daily_features.csv")

print("✅ Data loaded")
print(df[["city", "date", "avg_temperature"]].head())

# --------------------------------------------------
# STEP 2: Prepare data
# --------------------------------------------------
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by=["city", "date"])

# --------------------------------------------------
# STEP 3: Time-based train/test split + MA(5)
# --------------------------------------------------
results = []

for city in df["city"].unique():
    city_df = df[df["city"] == city].copy()

    # Need at least 6 days (5 for MA + 1 test)
    if len(city_df) < 6:
        print(f"⚠️ Not enough data for {city}, skipping")
        continue

    train = city_df.iloc[:-1]
    test = city_df.iloc[-1:]

    # --------------------------------------------------
    # STEP 4: MA(5) forecast
    # --------------------------------------------------
    last_5_avg = train.tail(5)["avg_temperature"].mean()
    actual = test.iloc[0]["avg_temperature"]

    error = abs(actual - last_5_avg)

    results.append({
        "city": city,
        "train_last_date": train.iloc[-1]["date"],
        "test_date": test.iloc[0]["date"],
        "ma_5_forecast": last_5_avg,
        "actual": actual,
        "absolute_error": error
    })

# --------------------------------------------------
# STEP 5: Evaluation summary
# --------------------------------------------------
results_df = pd.DataFrame(results)

print("\n📊 MA(5) Time-Series Results")
print(results_df)

print("\n📉 Mean Absolute Error (MA(5))")
print(results_df.groupby("city")["absolute_error"].mean())
