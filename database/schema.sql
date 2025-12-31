CREATE TABLE IF NOT EXISTS weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    region TEXT,
    country TEXT,
    temperature_c REAL,
    humidity INTEGER,
    wind_kph REAL,
    condition TEXT,
    api_last_updated TEXT,
    fetched_at_utc TEXT
);

-- Historical data (append-only)
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
);


-- Latest snapshot (one row per city)
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
);

CREATE TABLE IF NOT EXISTS weather_daily_summary (
    city TEXT NOT NULL,
    date TEXT NOT NULL,
    avg_temperature REAL,
    min_temperature REAL,
    max_temperature REAL,
    avg_humidity REAL,
    record_count INTEGER,
    PRIMARY KEY (city, date)
);


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
);
