"""1️⃣ What this file’s role is (in the project)
This file answers one question only:
“What does the daily weather time series look like across cities?”
It is:
Exploratory
One-time / occasional
Human-facing (plots + prints)"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

DB_PATH = "database/weather.db"
OUTPUT_DIR = "outputs/eda"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# Load daily summary
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

df["date"] = pd.to_datetime(df["date"])

print("✅ Daily summary loaded")
print(df)
# --------------------------------------------------
# Temperature trend per city
# --------------------------------------------------
for city in df["city"].unique():
    city_df = df[df["city"] == city]

    plt.figure()
    plt.plot(city_df["date"], city_df["avg_temperature"], marker="o")
    plt.title(f"Average Temperature Trend — {city}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)

    file_path = f"{OUTPUT_DIR}/temp_trend_{city.lower()}.png"
    plt.savefig(file_path)
    plt.close()

    print(f"📈 Saved temperature trend plot for {city}")
# --------------------------------------------------
# Humidity trend per city
# --------------------------------------------------
for city in df["city"].unique():
    city_df = df[df["city"] == city]

    plt.figure()
    plt.plot(city_df["date"], city_df["avg_humidity"], marker="o", color="orange")
    plt.title(f"Average Humidity Trend — {city}")
    plt.xlabel("Date")
    plt.ylabel("Humidity (%)")
    plt.grid(True)

    file_path = f"{OUTPUT_DIR}/humidity_trend_{city.lower()}.png"
    plt.savefig(file_path)
    plt.close()

    print(f"💧 Saved humidity trend plot for {city}")
# --------------------------------------------------
# City comparison: Temperature
# --------------------------------------------------
plt.figure()

for city in df["city"].unique():
    city_df = df[df["city"] == city]
    plt.plot(city_df["date"], city_df["avg_temperature"], marker="o", label=city)

plt.title("Average Temperature Comparison Across Cities")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.grid(True)

file_path = f"{OUTPUT_DIR}/temp_comparison_all_cities.png"
plt.savefig(file_path)
plt.close()

print("📊 Saved temperature comparison plot across cities")
# --------------------------------------------------
# Correlation analysis
# --------------------------------------------------
pivot_temp = df.pivot(index="date", columns="city", values="avg_temperature")
pivot_humidity = df.pivot(index="date", columns="city", values="avg_humidity")

print("\n📌 Temperature Correlation Across Cities")
print(pivot_temp.corr())

print("\n📌 Humidity Correlation Across Cities")
print(pivot_humidity.corr())
