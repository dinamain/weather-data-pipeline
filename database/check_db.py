import sqlite3

conn = sqlite3.connect("database/weather.db")
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM weather_data").fetchall()

for row in rows:
    print(row)

conn.close()

