"""This file will:

Load engineered daily data

Split per city by date

Run naive forecast on test period

Print test MAE

✅ Correct approach for time-series

You must respect time order.

Example (per city):

2025-12-31  → train
2026-01-02  → train
2026-01-03  → train
-------------------
2026-01-04  → test
2026-01-05  → test


👉 Past → Future only"""

import pandas as pd
# --------------------------------------------------
# STEP 1: Load engineered daily data
# --------------------------------------------------
df= pd.read_csv("outputs/engineered_daily_features.csv")
print("✅ Data loaded")
print(df[["city","date", "avg_temperature"]].head())
# --------------------------------------------------
# STEP 2: Prepare data
# --------------------------------------------------
df["date"]=pd.to_datetime(df["date"])
df=df.sort_values(by=["city", "date"])
# --------------------------------------------------
# STEP 3: Time-based train/test split
# Strategy:
# - Use last 1 day per city as TEST
# - All previous days as TRAIN
# --------------------------------------------------
results= []
for city in df["city"].unique():
    city_df = df[df["city"]==city].copy()

    if len(city_df)<3:
        print(f"⚠️ Not enough data for {city}, skipping")
        continue
    train=city_df.iloc[:-1]
    test=city_df.iloc[-1:]

    # --------------------------------------------------
    # STEP 4: Naive forecast
    # --------------------------------------------------
    last_train_temp = train.iloc[-1]["avg_temperature"]
    actual_temp =  test.iloc[0]["avg_temperature"]

    forecast = last_train_temp
    error = abs(actual_temp - forecast)

    results.append({
        "city": city,
        "train_last_date": train.iloc[-1]["date"],
        "test_date": test.iloc[0]["date"],
        "forecast": forecast,
        "actual": actual_temp,
        "absolute_error": error
    })
    
# --------------------------------------------------
# STEP 5: Evaluation summary
# --------------------------------------------------
results_df = pd.DataFrame(results)

print("\n📊 Time-Series Test Results")
print(results_df)

print("\n📉 Mean Absolute Error (Test Set)")
print(results_df.groupby("city")["absolute_error"].mean())