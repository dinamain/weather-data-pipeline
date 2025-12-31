import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt

# --------------------------------------------------
# Database connection
# --------------------------------------------------
DB_PATH = "database/weather.db"

if not os.path.exists(DB_PATH):
    print("❌ Database not found.")
    exit(1)

conn = sqlite3.connect(DB_PATH)

query = "SELECT * FROM weather_data"
df = pd.read_sql_query(query, conn)

conn.close()

# --------------------------------------------------
# Validate data
# --------------------------------------------------
if df.empty:
    print("⚠️ No data found in database.")
    exit(0)

print("✅ Data loaded from SQLite")
print(df.head())

# --------------------------------------------------
# Time conversion
# --------------------------------------------------
df["fetched_at_utc"] = pd.to_datetime(df["fetched_at_utc"])
df["api_last_updated"] = pd.to_datetime(df["api_last_updated"])

# Sort for time-series correctness
df = df.sort_values("fetched_at_utc")

print("✅ Time columns converted and sorted")

# --------------------------------------------------
# Export cleaned data
# --------------------------------------------------
os.makedirs("outputs", exist_ok=True)

csv_path = "outputs/cleaned_weather_data.csv"
df.to_csv(csv_path, index=False)

print(f"✅ Cleaned data exported to {csv_path}")

# --------------------------------------------------
# Simple analysis
# --------------------------------------------------
avg_temp = df["temperature_c"].mean()
max_temp = df["temperature_c"].max()
min_temp = df["temperature_c"].min()

print("\n📈 Temperature Summary")
print(f"Average Temperature: {avg_temp:.2f} °C")
print(f"Maximum Temperature: {max_temp:.2f} °C")
print(f"Minimum Temperature: {min_temp:.2f} °C")

# --------------------------------------------------
# Plot temperature trend
# --------------------------------------------------
os.makedirs("outputs/plots", exist_ok=True)

plt.figure()
plt.plot(df["fetched_at_utc"], df["temperature_c"])
plt.xlabel("Time (UTC)")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Trend Over Time")
plt.xticks(rotation=45)
plt.tight_layout()

plot_path = "outputs/plots/temperature_trend.png"
plt.savefig(plot_path)
plt.close()

print(f"\n📊 Temperature trend plot saved to {plot_path}")
