import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv

from weather import save_weather_to_csv


load_dotenv(".env")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'weather_data_pipeline',
    default_args=default_args,
    description='Pipeline for fetching weather data every minute',
    schedule_interval=timedelta(minutes=1),
    catchup=False,
)


def fetch_and_save_weather():
    api_key = os.getenv("API_KEY")
    csv_path = "weather.csv"
    city = "Moscow"
    return save_weather_to_csv(api_key=api_key, csv_path=csv_path, city=city)


weather_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch_and_save_weather,
    dag=dag,
)
