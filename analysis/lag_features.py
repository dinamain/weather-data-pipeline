import sqlite3
import pandas as pd 

#1. LOAD DATA FROM DATABASE
conn = sqlite3.connect("database/weather.db")

query = """
SELECT city,
temperature_c, fetched_at_utc
FROM weather_history
ORDER BY city, fetched_at_utc
"""
df = pd.read_sql(query, conn)
conn.close()

print("DATA LOADED")
print(df.head())

#2. CONVERT TIMESTAMP
df["fetched_at_utc"]= pd.to_datetime(df["fetched_at_utc"])

#3. CREATE LAG FEATURES PER CITY
df["temp_lag_1"]=df.groupby("city")["temperature_c"].shift(1)
df["temp_lag_24"] = df.groupby("city")["temperature_c"].shift(24)

#4. DROP ROWS WITHOUT ENOUGH HISTORY
df_clean = df.dropna()

print("\n📊 Lag Feature Sample")
print(df_clean.head())

#5. SAVE OUTPUT
df_clean.to_csv("outputs/temperature_lag_features.csv", index=False)

print("\n📁 Saved: outputs/temperature_lag_features.csv")
print(f"Rows after lagging: {len(df_clean)}")