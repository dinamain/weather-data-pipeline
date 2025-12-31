import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt

DB_PATH = "database/weather.db"

conn = sqlite3.connect(DB_PATH)

# --------------------------------------------------
# Load daily summary data
# --------------------------------------------------
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
    print("⚠️ No data available for cross-city analysis.")
    exit(0)

df["date"] = pd.to_datetime(df["date"])

print("✅ Daily summary data loaded")
print(df.head())

# --------------------------------------------------
# Hottest city (average temperature)
# --------------------------------------------------
city_avg_temp = (
    df.groupby("city")["avg_temperature"]
    .mean()
    .sort_values(ascending=False)
)

print("\n🔥 Average Temperature by City")
print(city_avg_temp)

# --------------------------------------------------
# Temperature variability (max - min)
# --------------------------------------------------
df["temp_range"] = df["max_temperature"] - df["min_temperature"]

city_variability = (
    df.groupby("city")["temp_range"]
    .mean()
    .sort_values(ascending=False)
)

print("\n📉 Temperature Variability by City")
print(city_variability)

# --------------------------------------------------
# Cross-city temperature trend plot
# --------------------------------------------------
os.makedirs("outputs/plots", exist_ok=True)

plt.figure()

for city in df["city"].unique():
    city_df = df[df["city"] == city]
    plt.plot(city_df["date"], city_df["avg_temperature"], label=city)

plt.xlabel("Date")
plt.ylabel("Average Temperature (°C)")
plt.title("Daily Average Temperature Comparison Across Cities")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plot_path = "outputs/plots/cross_city_temperature_trend.png"
plt.savefig(plot_path)
plt.close()

print(f"\n📊 Cross-city temperature trend saved to {plot_path}")
