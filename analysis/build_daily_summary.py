import sqlite3
from datetime import datetime

DB_PATH = "database/weather.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --------------------------------------------------
# Create daily summary table
# --------------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_daily_summary (
    city TEXT NOT NULL,
    date TEXT NOT NULL,
    avg_temperature REAL,
    min_temperature REAL,
    max_temperature REAL,
    avg_humidity REAL,
    record_count INTEGER,
    PRIMARY KEY (city, date)
)
""")

# --------------------------------------------------
# Build daily aggregation from history
# --------------------------------------------------
aggregation_query = """
INSERT OR REPLACE INTO weather_daily_summary
SELECT
    city,
    DATE(datetime(fetched_at_utc, '+5 hours', '+30 minutes'))
 AS date,
    AVG(temperature_c) AS avg_temperature,
    MIN(temperature_c) AS min_temperature,
    MAX(temperature_c) AS max_temperature,
    AVG(humidity) AS avg_humidity,
    COUNT(*) AS record_count
FROM weather_history
GROUP BY city, DATE(api_last_updated)
"""

cursor.execute(aggregation_query)
conn.commit()
conn.close()

print("✅ Daily weather summary table built successfully")
