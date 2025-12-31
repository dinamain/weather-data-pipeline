import requests
import yaml
import sqlite3
import os
from datetime import datetime, timezone
import logging
import time

# --------------------------------------------------
# Logging configuration
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("outputs/ingestion.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Load configuration
# --------------------------------------------------
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

weather_config = config["weatherapi"]
url = weather_config["base_url"]
cities = weather_config["cities"]

# --------------------------------------------------
# SQLite setup
# --------------------------------------------------
os.makedirs("database", exist_ok=True)
db_path = "database/weather.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# --------------------------------------------------
# Create tables
# --------------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    region TEXT,
    country TEXT,
    temperature_c REAL,
    humidity INTEGER,
    wind_kph REAL,
    condition TEXT,
    api_last_updated TEXT NOT NULL,
    fetched_at_utc TEXT,
    UNIQUE(city, api_last_updated)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_current (
    city TEXT PRIMARY KEY,
    region TEXT,
    country TEXT,
    temperature_c REAL,
    humidity INTEGER,
    wind_kph REAL,
    condition TEXT,
    api_last_updated TEXT,
    fetched_at_utc TEXT
)
""")
def fetch_with_retry(url, params, retries=3, timeout=10):
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, timeout=timeout)

            if response.status_code == 200:
                return response

            logger.warning(
                f"Attempt {attempt}: Non-200 response "
                f"({response.status_code}) for {params.get('q')}"
            )

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Attempt {attempt}: Request failed for "
                f"{params.get('q')} — {e}"
            )

        time.sleep(2 * attempt)  # exponential backoff

    return None

# --------------------------------------------------
# Ingestion loop (THIS IS THE FIX)
# --------------------------------------------------
for city in cities:
    params = {
        "key": weather_config["api_key"],
        "q": city
    }

    response = fetch_with_retry(url, params)

    if response is None:
        logger.error(f"❌ Failed to fetch data for {city} after retries")
        continue

    print(f"\n➡️ Fetching city: {city}, status: {response.status_code}")

    if response.status_code != 200:
        print(f"❌ API call failed for {city}")
        continue

    data = response.json()

    location = data.get("location", {})
    current = data.get("current", {})
    condition = current.get("condition", {})

    cleaned_weather = {
        "city": city,
        "region": location.get("region", ""),
        "country": location.get("country", ""),
        "temperature_c": float(current.get("temp_c", 0.0)),
        "humidity": int(current.get("humidity", 0)),
        "wind_kph": float(current.get("wind_kph", 0.0)),
        "condition": condition.get("text", "Unknown"),
        "api_last_updated": current.get("last_updated", ""),
        "fetched_at_utc": datetime.now(timezone.utc).isoformat()
    }

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------
    if cleaned_weather["humidity"] > 100:
        print("⚠️ Warning: Humidity over 100%")

    if not cleaned_weather["api_last_updated"]:
        print("⚠️ Missing api_last_updated — skipping")
        continue

    # --------------------------------------------------
    # Insert into weather_history (idempotent)
    # --------------------------------------------------
    try:
        cursor.execute("""
        INSERT INTO weather_history (
            city, region, country,
            temperature_c, humidity, wind_kph,
            condition, api_last_updated, fetched_at_utc
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cleaned_weather["city"],
            cleaned_weather["region"],
            cleaned_weather["country"],
            cleaned_weather["temperature_c"],
            cleaned_weather["humidity"],
            cleaned_weather["wind_kph"],
            cleaned_weather["condition"],
            cleaned_weather["api_last_updated"],
            cleaned_weather["fetched_at_utc"]
        ))

        conn.commit()
        logger.info(f"Inserted into weather_history for {city}")


    except sqlite3.IntegrityError:
        logger.warning(f"Duplicate history record skipped for {city}")


    # --------------------------------------------------
    # Upsert into weather_current
    # --------------------------------------------------
    cursor.execute("""
    INSERT OR REPLACE INTO weather_current (
        city, region, country,
        temperature_c, humidity, wind_kph,
        condition, api_last_updated, fetched_at_utc
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        cleaned_weather["city"],
        cleaned_weather["region"],
        cleaned_weather["country"],
        cleaned_weather["temperature_c"],
        cleaned_weather["humidity"],
        cleaned_weather["wind_kph"],
        cleaned_weather["condition"],
        cleaned_weather["api_last_updated"],
        cleaned_weather["fetched_at_utc"]
    ))

    conn.commit()
    logger.info(f"weather_current updated for {city}")


# --------------------------------------------------
# Close DB
# --------------------------------------------------
conn.close()
print("\n🎉 Ingestion run completed for all cities")
