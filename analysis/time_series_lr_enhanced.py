import pandas as pd
from sklearn.linear_model import LinearRegression

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
# STEP 3: Create MODEL-SPECIFIC lag features
# --------------------------------------------------
df["temp_lag_2d"] = df.groupby("city")["avg_temperature"].shift(2)
df["temp_lag_3d"] = df.groupby("city")["avg_temperature"].shift(3)

# --------------------------------------------------
# STEP 4: Create short-window rolling features
# --------------------------------------------------
df["temp_rolling_3d"] = (
    df.groupby("city")["avg_temperature"]
      .rolling(window=3)
      .mean()
      .shift(1)
      .reset_index(level=0, drop=True)
)

df["temp_volatility_3d"] = (
    df.groupby("city")["avg_temperature"]
      .rolling(window=3)
      .std()
      .shift(1)
      .reset_index(level=0, drop=True)
)


# --------------------------------------------------
# STEP 5: Define features and target
# --------------------------------------------------
FEATURES = [
    "temp_lag_1d",
    "temp_lag_2d",
    "temp_lag_3d",
    "temp_rolling_3d",
    "temp_volatility_3d",
]

TARGET = "avg_temperature"

results = []

# --------------------------------------------------
# STEP 6: Time-series train/test per city
# --------------------------------------------------
for city in df["city"].unique():
    city_df = df[df["city"] == city].copy()

    city_df = city_df.dropna(subset=FEATURES + [TARGET])

    if len(city_df) < 5:
        print(f"⚠️ Not enough data for {city}, skipping")
        continue

    train = city_df.iloc[:-1]
    test = city_df.iloc[-1:]

    X_train = train[FEATURES]
    y_train = train[TARGET]

    X_test = test[FEATURES]
    y_test = test[TARGET]

    # --------------------------------------------------
    # STEP 7: Train Linear Regression
    # --------------------------------------------------
    model = LinearRegression()
    model.fit(X_train, y_train)

    forecast = model.predict(X_test)[0]
    error = abs(y_test.values[0] - forecast)

    results.append({
        "city": city,
        "test_date": test.iloc[0]["date"],
        "forecast": forecast,
        "actual": y_test.values[0],
        "absolute_error": error,
    })

# --------------------------------------------------
# STEP 8: Evaluation
# --------------------------------------------------
results_df = pd.DataFrame(results)

print("\n📊 Enhanced Linear Regression Results")
print(results_df)

print("\n📉 Mean Absolute Error (Enhanced LR)")
print(results_df.groupby("city")["absolute_error"].mean())
