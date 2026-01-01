
REM Example script for scheduling ingestion via Windows Task Scheduler

@echo off
cd /d C:\Users\dinau\OneDrive\Desktop\2025\project\weather-data-pipeline
call venv\Scripts\activate
python ingestion\fetch_weather.py
