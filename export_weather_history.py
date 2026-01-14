import sqlite3
import pandas as pd
from pathlib import Path

# 1. Paths
DB_PATH = "database/weather.db"
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "weather_history_latest.csv"

# 2. Connect to database
conn = sqlite3.connect(DB_PATH)

# 3. Read full table
query = """
SELECT *
FROM weather_history
ORDER BY fetched_at_utc
"""

df = pd.read_sql(query, conn)

conn.close()

# 4. Save to CSV
df.to_csv(OUTPUT_FILE, index=False)

# 5. Confirmation
print("✅ Fresh weather history exported")
print(f"📁 Rows exported: {len(df)}")
print(f"📄 File saved as: {OUTPUT_FILE}")
