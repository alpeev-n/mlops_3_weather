from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.weather import save_weather


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 2, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'weather_dag',
    default_args=default_args,
    description='Fetch weather every minute and save to CSV',
    schedule_interval='* * * * *',
    catchup=False,
)

fetch_weather_task = PythonOperator(
    task_id='fetch_and_save_weather',
    python_callable=save_weather,
    dag=dag
)
