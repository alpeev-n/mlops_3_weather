from __future__ import annotations

import os
import sys
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv

from weather import append_weather_to_csv


def fetch_and_save_weather() -> None:
    """
    Load API key from .env and append current Moscow weather to CSV.
    """
    root = os.environ.get("AIRFLOW_HOME", _PROJECT_ROOT)
    load_dotenv(os.path.join(root, ".env"))
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY is not set in .env")

    csv_path = os.path.join(root, "weather.csv")
    append_weather_to_csv(api_key=api_key, city="Moscow", csv_path=csv_path)


with DAG(
    dag_id="weather_to_csv",
    description="Fetch Moscow weather every minute and append to weather.csv",
    start_date=datetime(2026, 2, 9),
    schedule_interval="* * * * *", 
    catchup=False,
    tags=["weather"],
) as dag:
    fetch_weather_task = PythonOperator(
        task_id="fetch_and_save_weather",
        python_callable=fetch_and_save_weather,
    )

