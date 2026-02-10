from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from weather import get_weather
import os


api_key = os.getenv("API_KEY")
city = "Moscow"
filename = "/opt/airflow/data/weather.csv"


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 100,
    'retry_delay': timedelta(minutes=1),
}


dag = DAG(
    'weather_dag',
    default_args=default_args,
    description='A DAG to fetch weather data and save it to CSV',
    schedule_interval=timedelta(minutes=1),
    catchup=False,
)


with dag:
    fetch_and_save_weather = PythonOperator(
        task_id='fetch_and_save_weather',
        python_callable=get_weather,
        op_kwargs={
            'api_key': api_key,
            'city': city,
            'filename': filename,
        },
    )

    fetch_and_save_weather