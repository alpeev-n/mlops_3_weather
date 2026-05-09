import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow.decorators import dag, task


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from weather import collect_weather


DAG_ID = "moscow_weather_pipeline"
DAG_START_DATE = datetime(2026, 5, 9)
DAG_SCHEDULE = timedelta(minutes=1)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=30),
}


@dag(
    dag_id=DAG_ID,
    description="Pipeline for collecting Moscow weather data from OpenWeatherMap",
    default_args=default_args,
    start_date=DAG_START_DATE,
    schedule=DAG_SCHEDULE,
    catchup=False,
    tags=["mlops", "weather", "openweathermap"],
)
def moscow_weather_pipeline():
    """DAG для регулярного сбора погодных данных по Москве"""

    @task(task_id="collect_weather")
    def collect_weather_task() -> str:
        """получает текущую погоду и добавляет новую строку в weather.csv"""
        return collect_weather()

    collect_weather_task()


moscow_weather_pipeline()