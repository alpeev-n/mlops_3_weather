from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import conf

from weather import collect_weather

default_args = {
    "owner": "Petr Kreslin",
    "start_date": datetime(2026, 5, 5),
}

dags_path = conf.get("core", "dags_folder")

with DAG(
    dag_id="weather_moscow",
    default_args=default_args,
    start_date=datetime(2026, 5, 6),
    schedule="* * * * *",
    catchup=False,
    description="Open Weather Moscow",
) as dag:

    collect_weather_moscow = PythonOperator(
        task_id="collect_weather_task",
        python_callable=collect_weather,
        op_kwargs={"city": "Moscow", "path": dags_path},
    )


    collect_weather_moscow
