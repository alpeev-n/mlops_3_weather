import logging
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable

sys.path.insert(0, "/opt/airflow")

from weather import fetch_and_save_weather

log = logging.getLogger(__name__)


def _fetch_weather():
    city = Variable.get("WEATHER_CITY", default_var="Moscow")
    csv_path = "/opt/airflow/weather.csv"
    log.info("Fetching weather for city: %s", city)
    fetch_and_save_weather(city, csv_path)
    log.info("Weather data saved to %s", csv_path)


with DAG(
    dag_id="weather_fetch",
    schedule_interval="*/1 * * * *",
    start_date=datetime(2026, 5, 10),
    catchup=False,
    tags=["weather"],
) as dag:
    fetch_task = PythonOperator(
        task_id="fetch_and_save_weather",
        python_callable=_fetch_weather,
    )
