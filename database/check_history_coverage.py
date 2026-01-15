import sqlite3
import pandas as pd

conn = sqlite3.connect("database/weather.db")

query = """
SELECT
  city,
  DATE(fetched_at_utc) AS date,
  COUNT(*) AS records
FROM weather_history
GROUP BY city, DATE(fetched_at_utc)
ORDER BY city, date;
"""

df = pd.read_sql_query(query, conn)
conn.close()

print(df)
