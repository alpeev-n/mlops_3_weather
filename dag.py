import os
from datetime import datetime

from airflow.decorators import dag, task
from airflow.models import Variable
from dotenv import load_dotenv

from weather import append_weather_csv


@dag(
    dag_id="weather",
    schedule_interval="*/1 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
)
def weather():
    @task
    def append_weather_csv_wrapper():
        api_key = Variable.get("API_KEY")
        append_weather_csv(api_key, city="Moscow")
    
    append_weather_csv_wrapper()


dag_instance = weather()

