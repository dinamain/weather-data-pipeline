import sqlite3
import pandas as pd

DB_PATH = "database/weather.db"

# --------------------------------------------------
# Connect to database
# --------------------------------------------------
conn = sqlite3.connect(DB_PATH)

# --------------------------------------------------
# 1. Drop existing daily summary (important)
# --------------------------------------------------
conn.execute("DROP TABLE IF EXISTS weather_daily_summary")
conn.commit()

print("🗑️ Old weather_daily_summary dropped")

# --------------------------------------------------
# 2. Rebuild daily summary from raw history
# --------------------------------------------------
query = """
CREATE TABLE weather_daily_summary AS
SELECT
    city,
    DATE(fetched_at_utc) AS date,
    AVG(temperature_c) AS avg_temperature,
    MIN(temperature_c) AS min_temperature,
    MAX(temperature_c) AS max_temperature,
    AVG(humidity) AS avg_humidity,
    COUNT(*) AS records_count
FROM weather_history
GROUP BY city, DATE(fetched_at_utc)
ORDER BY city, date;
"""

conn.execute(query)
conn.commit()

print("✅ weather_daily_summary rebuilt successfully")

# --------------------------------------------------
# 3. Verify result
# --------------------------------------------------
df = pd.read_sql_query(
    "SELECT * FROM weather_daily_summary ORDER BY city, date",
    conn
)

conn.close()

print("\n📊 Daily Summary Preview")
print(df.head(10))
print(f"\nTotal daily rows: {len(df)}")
