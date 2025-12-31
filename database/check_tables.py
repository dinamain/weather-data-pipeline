import sqlite3

conn = sqlite3.connect("database/weather.db")
cursor = conn.cursor()

print("\n--- weather_history ---")
for row in cursor.execute("SELECT * FROM weather_history"):
    print(row)

print("\n--- weather_current ---")
for row in cursor.execute("SELECT * FROM weather_current"):
    print(row)

conn.close()
