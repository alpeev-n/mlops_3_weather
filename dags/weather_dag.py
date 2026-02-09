from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.weather import get_weather_data, save_to_csv

def collect_weather_data():
    """Задача для Airflow: получить погоду и сохранить в CSV."""
    data = get_weather_data()
    if data:
        # Путь к файлу
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'weather.csv')
        save_to_csv(data, csv_path)
        print(f"Данные успешно сохранены в {csv_path}")
    else:
        print("Не удалось получить данные о погоде")

# Аргументы DAG
default_args = {
    'owner': 'student',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Определение DAG
with DAG(
    dag_id='weather_collection_dag',          
    default_args=default_args,
    description='Ежедневный сбор данных о погоде',
    schedule_interval='*/1 * * * *',          # Каждую минуту для теста
    start_date=datetime(2024, 2, 9),          # Дата начала
    catchup=False,                            
    tags=['weather', 'homework'],
) as dag:

    # Задача
    collect_weather_task = PythonOperator(
        task_id='collect_weather_task',
        python_callable=collect_weather_data,
    )

    collect_weather_task