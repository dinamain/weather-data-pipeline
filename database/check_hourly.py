import sqlite3

conn = sqlite3.connect("database/weather.db")
cursor = conn.cursor()

print("\n--- weather_hourly_summary ---")
for row in cursor.execute("SELECT * FROM weather_hourly_summary"):
    print(row)

conn.close()
