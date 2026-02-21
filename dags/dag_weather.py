from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from weather.weather import save_weather_to_csv


args = {
    "owner": "alena",
    'start_date': datetime(2026, 2, 15),
    'email': ["alis.from.wonderland@mail.ru"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    dag_id="weather_moscow",
    catchup=False,
    default_args=args,
    start_date=datetime(2026, 2, 15),
    schedule_interval="*/1 * * * *",
    tags=["weather"]
) as dag:

    fetch_weather_task = PythonOperator(
        task_id="fetch_weather",
        python_callable=save_weather_to_csv,
    )
