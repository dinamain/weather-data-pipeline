import sqlite3

DB_PATH = "database/weather.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --------------------------------------------------
# Create hourly summary table
# --------------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_hourly_summary (
    city TEXT NOT NULL,
    date TEXT NOT NULL,
    hour INTEGER NOT NULL,
    avg_temperature REAL,
    min_temperature REAL,
    max_temperature REAL,
    avg_humidity REAL,
    record_count INTEGER,
    PRIMARY KEY (city, date, hour)
)
""")

# --------------------------------------------------
# Build hourly aggregation from history
# --------------------------------------------------
aggregation_query = """
INSERT OR REPLACE INTO weather_hourly_summary
SELECT
    city,
    DATE(api_last_updated) AS date,
    CAST(STRFTIME('%H', api_last_updated) AS INTEGER) AS hour,
    AVG(temperature_c) AS avg_temperature,
    MIN(temperature_c) AS min_temperature,
    MAX(temperature_c) AS max_temperature,
    AVG(humidity) AS avg_humidity,
    COUNT(*) AS record_count
FROM weather_history
GROUP BY city, DATE(api_last_updated), hour
"""

cursor.execute(aggregation_query)
conn.commit()
conn.close()

print("✅ Hourly weather summary table built successfully")
