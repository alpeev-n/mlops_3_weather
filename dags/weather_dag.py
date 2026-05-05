from datetime import datetime
from airflow.decorators import dag, task


@dag(
    dag_id='weather_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule='* * * * *',
    catchup=False,
)
def weather_pipeline():

    @task
    def collect_weather():
        import os
        from dotenv import load_dotenv
        from weather import fetch_weather

        load_dotenv('/opt/airflow/project/.env')
        api_key = os.getenv('API_KEY')
        fetch_weather(api_key=api_key)

    collect_weather()  # вот эта строка


weather_pipeline()
