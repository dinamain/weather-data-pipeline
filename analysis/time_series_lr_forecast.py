"""LINEAR REGRESSION WITH LAG FEATURES (1-3 DAYS)
GOA; :
PREDICT NEXT DAYS AVEG TEMP USINGF THE PAST 3 DAYS .


METHOD:
PER CITY MODELLING 
TIME BASED TRAIN TEST SPLIT
NO DATA LEAKAGE"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# --------------------------------------------------
# STEP 1: Load engineered daily data
# --------------------------------------------------
df= pd.read_csv("outputs/engineered_daily_features.csv")
df["date"]=pd.to_datetime(df["date"])
df=df.sort_values(by=["city","date"])

print("✅ Data loaded")
print(df[["city", "date", "avg_temperature"]].head())
# --------------------------------------------------
# STEP 2: Create additional lag features
# --------------------------------------------------
df["temp_lag_2d"]=df.groupby("city")["avg_temperature"].shift(2)
df["temp_lag_3d"]=df.groupby("city")["avg_temperature"].shift(3)
# --------------------------------------------------
# STEP 3: Model per city
# --------------------------------------------------
results=[]
for city in df["city"].unique():
    city_df = df[df["city"]==city].copy()
            # Keep only rows with full lag data
    city_df = city_df.dropna(subset=["temp_lag_1d", "temp_lag_2d","temp_lag_3d"]
                             )
    if len(city_df)<5:
        print(f"⚠️ Not enough data for {city}, skipping")
        continue

    # --------------------------------------------------
    # STEP 4: Time-based train/test split
    # --------------------------------------------------
    train=city_df.iloc[:-1]
    test=city_df.iloc[-1:]
    X_train = train[["temp_lag_1d", "temp_lag_2d", "temp_lag_3d"]]
    y_train = train["avg_temperature"]

    X_test = test[["temp_lag_1d", "temp_lag_2d", "temp_lag_3d"]]
    y_test = test["avg_temperature"]

    # --------------------------------------------------
    # STEP 5: Train model
    # --------------------------------------------------
    model = LinearRegression()
    model.fit(X_train, y_train)

    prediction = model.predict(X_test)[0]
    error = abs(y_test.values[0] - prediction)

    results.append({
        "city": city,
        "test_date": test.iloc[0]["date"],
        "prediction": prediction,
        "actual": y_test.values[0],
        "absolute_error": error,
        "coef_lag_1d": model.coef_[0],
        "coef_lag_2d": model.coef_[1],
        "coef_lag_3d": model.coef_[2],
    })

# --------------------------------------------------
# STEP 6: Results
# --------------------------------------------------
results_df = pd.DataFrame(results)

print("\n📊 Linear Regression Forecast Results")
print(results_df)

print("\n📉 Mean Absolute Error (Linear Regression)")
print(results_df.groupby("city")["absolute_error"].mean())