# database/check_city_ranges.py
import sqlite3
import pandas as pd

conn = sqlite3.connect("database/weather.db")

query = """
SELECT
  city,
  MIN(temperature_c) AS min_temp,
  MAX(temperature_c) AS max_temp,
  AVG(temperature_c) AS avg_temp,
  COUNT(*) AS records
FROM weather_history
GROUP BY city
"""

df = pd.read_sql_query(query, conn)
conn.close()

print(df)
