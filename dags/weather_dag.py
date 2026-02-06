from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from weather import fetch_weather, save_weather_data
import os
from dotenv import load_dotenv


def fetch_and_save_weather():
    """Task function for Airflow to fetch and save weather data."""
    load_dotenv(os.path.join(project_root, ".env"))
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        raise ValueError("API_KEY not found in .env file")
    
    # Fetch weather data
    weather_data = fetch_weather(api_key=api_key)
    
    # Save to CSV
    csv_path = os.path.join(project_root, "weather.csv")
    save_weather_data(weather_data, csv_file=csv_path)


# Default arguments for DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime(2026, 2, 7),
}

# Create DAG
dag = DAG(
    'weather_collection',
    default_args=default_args,
    description='Collect weather data from OpenWeatherMap API every minute',
    schedule_interval='*/1 * * * *',  # Every minute
    catchup=False,
    tags=['weather', 'data-collection'],
)

# Create task
fetch_weather_task = PythonOperator(
    task_id='fetch_and_save_weather',
    python_callable=fetch_and_save_weather,
    dag=dag,
)

fetch_weather_task
