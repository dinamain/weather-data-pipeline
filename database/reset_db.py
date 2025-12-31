import sqlite3

conn = sqlite3.connect("database/weather.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS weather_history")
cursor.execute("DROP TABLE IF EXISTS weather_current")

conn.commit()
conn.close()

print("✅ Database reset complete")
