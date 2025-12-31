# 🌦️ API-Based Weather Data Ingestion & Analytics Pipeline

## 📖 Overview
This project is an end-to-end **API-based data ingestion and analytics pipeline** built using Python and SQLite.  
It demonstrates how real-world data systems ingest external APIs, ensure data correctness, maintain historical records, and generate analytical insights.

The system is designed with **production-minded principles** such as idempotent ingestion, separation of concerns, scalable configuration, aggregation layers, and logging with retries.

---

## 🎯 Key Features
- Multi-city weather data ingestion from public API
- Config-driven architecture (no hardcoded cities)
- Idempotent ingestion with database-level constraints
- Snapshot vs history table design
- Daily and hourly aggregation tables (warehouse-style)
- Cross-city comparative analytics
- Structured logging with retries and timeouts
- SQLite-backed persistence
- CSV and plot-based outputs

---

## 🏗️ System Architecture

Weather API
↓
Ingestion Layer (Python + Requests)
↓
Validation & Cleaning
↓
SQLite Database
├── weather_history (immutable snapshots)
├── weather_current (latest per city)
├── weather_daily_summary
└── weather_hourly_summary
↓
Analytics Layer (Pandas + SQL)
↓
CSV Outputs & Plots

---

## 🗂️ Project Structure

weather-data-pipeline/
│
├── config/
│ └── config.yaml
│
├── ingestion/
│ └── fetch_weather.py
│
├── database/
│ ├── weather.db
│ ├── reset_db.py
│ ├── check_tables.py
│ └── check_summary.py
│
├── analysis/
│ ├── analyze_weather.py
│ ├── build_daily_summary.py
│ ├── build_hourly_summary.py
│ └── cross_city_analysis.py
│
├── outputs/
│ ├── cleaned_weather_data.csv
│ ├── plots/
│ └── ingestion.log
│
├── requirements.txt
└── README.md


---

## 🧠 Data Modeling Design

### 1️⃣ weather_history
- Append-only table
- Stores all raw snapshots
- Prevents duplicates using `(city, api_last_updated)` constraint

### 2️⃣ weather_current
- One row per city
- Always represents latest weather snapshot
- Updated using UPSERT logic

### 3️⃣ Aggregation Tables
- `weather_daily_summary`: per-city daily metrics
- `weather_hourly_summary`: per-city hourly metrics

This mirrors **real data warehouse design**.

---

## 🔁 Ingestion Logic
- API calls wrapped with retry & exponential backoff
- Timeouts to prevent hanging requests
- Partial failures handled gracefully (one city failure doesn’t stop pipeline)
- Logs written to both console and file

---

## 📊 Analytics Capabilities
- Daily & hourly temperature summaries
- Cross-city average temperature comparison
- Temperature variability analysis
- Time-series trend visualization
- CSV exports for downstream use

---

## ▶️ How to Run

### 1️⃣ Setup environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

2️⃣ Configure cities

Edit config/config.yaml:

cities:
  - Kochi
  - Bangalore
  - Mumbai

  3️⃣ Run ingestion
python ingestion/fetch_weather.py

4️⃣ Build aggregations
python analysis/build_daily_summary.py
python analysis/build_hourly_summary.py

5️⃣ Run analytics
python analysis/cross_city_analysis.py

Future Enhancements

Switchable API providers (WeatherAPI ↔ OpenWeatherMap)

Automated scheduling (cron / task scheduler)

Anomaly detection

Postgres migration

Dashboard visualization


Tech Stack

Python

Requests

SQLite

Pandas

Matplotlib

YAML

Logging