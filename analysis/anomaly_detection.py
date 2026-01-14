"""1️⃣ What this file is meant to do

This file answers:

“Did something unusual happen in daily temperature changes for each city?”

It does statistical anomaly detection on:

day-over-day temperature change

per city

using z-score"""

import sqlite3
import pandas as pd
import numpy as np
import os

DB_PATH = "database/weather.db"
OUTPUT_DIR = "outputs"
ALERT_DIR = "alerts"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ALERT_DIR, exist_ok=True)

# --------------------------------------------------
# Load daily summary data
# --------------------------------------------------
conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    city,
    date,
    avg_temperature
FROM weather_daily_summary
ORDER BY city, date
"""

df = pd.read_sql_query(query, conn)
conn.close()

df["date"] = pd.to_datetime(df["date"])

print("✅ Daily weather summary loaded")
print(df)

# --------------------------------------------------
# Compute day-over-day temperature change
# --------------------------------------------------
df["temp_change"] = df.groupby("city")["avg_temperature"].diff()

# --------------------------------------------------
# Z-score calculation (city-wise, safe)
# --------------------------------------------------
def compute_zscore(series):
    """
    Compute z-score safely.
    Returns NaN if standard deviation is zero or data is insufficient.
    """
    if series.std() == 0 or series.isna().all():
        return pd.Series([np.nan] * len(series))
    return (series - series.mean()) / series.std()

df["z_score"] = df.groupby("city")["temp_change"].transform(compute_zscore)

# --------------------------------------------------
# Anomaly flagging
# --------------------------------------------------
df["is_anomaly"] = df["z_score"].abs() > 2

# --------------------------------------------------
# Anomaly severity (magnitude of deviation)
# --------------------------------------------------
df["anomaly_severity"] = df["z_score"].abs()

# --------------------------------------------------
# Export results
# --------------------------------------------------
# Full anomaly analysis
full_output_path = os.path.join(OUTPUT_DIR, "anomalies.csv")
df.to_csv(full_output_path, index=False)

print(f"\n📁 Full anomaly analysis saved to {full_output_path}")

# Only confirmed anomalies
anomalies = df[df["is_anomaly"]]

if not anomalies.empty:
    alert_path = os.path.join(ALERT_DIR, "temperature_anomalies.csv")
    anomalies.to_csv(alert_path, index=False)
    print(f"🚨 {len(anomalies)} anomalies detected and saved to {alert_path}")
else:
    print("✅ No anomalies detected — system behavior within normal range")

# --------------------------------------------------
# Final console view (for inspection)
# --------------------------------------------------
print("\n🔍 Anomaly Detection Summary")
print(df[["city", "date", "avg_temperature", "temp_change", "z_score", "is_anomaly"]])
