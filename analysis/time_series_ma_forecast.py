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
# STEP 3: Time-based train/test MA forecast
# --------------------------------------------------
WINDOW = 3  # 3-day moving average
results = []

for city in df["city"].unique():
    city_df = df[df["city"] == city].copy()

    # Need at least WINDOW + 1 days
    if len(city_df) < WINDOW + 1:
        print(f"⚠️ Not enough data for {city}, skipping")
        continue

    # Train/Test split
    train = city_df.iloc[:-1]
    test = city_df.iloc[-1]

    # --------------------------------------------------
    # STEP 4: Moving Average Forecast
    # --------------------------------------------------
    last_n_days = train.tail(WINDOW)["avg_temperature"]
    forecast = last_n_days.mean()
    actual = test["avg_temperature"]

    error = abs(actual - forecast)

    results.append({
        "city": city,
        "train_last_date": train.iloc[-1]["date"],
        "test_date": test["date"],
        "ma_window": WINDOW,
        "forecast": forecast,
        "actual": actual,
        "absolute_error": error
    })

# --------------------------------------------------
# STEP 5: Evaluation summary
# --------------------------------------------------
results_df = pd.DataFrame(results)

print("\n📊 Moving Average Time-Series Results")
print(results_df)

print("\n📉 Mean Absolute Error (MA Forecast)")
print(results_df.groupby("city")["absolute_error"].mean())
