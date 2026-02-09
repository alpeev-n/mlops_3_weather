from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from weather import save_weather_to_csv


# Настройки DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 2, 6),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    "retry_delay": timedelta(seconds=30),  # Короткая задержка для минутных интервалов
    "execution_timeout": timedelta(minutes=2),
}

dag = DAG(
    'weather_collector',
    default_args=default_args,
    description='Пайплайн получения и сохранения погодных данных',
    schedule_interval="* * * * *",
    catchup=False,
    tags=['weather', 'api', 'csv'],
    max_active_runs=1,  # Защита от параллельных запусков
)

# Определение задач
save_weather_to_csv_task = PythonOperator(
    task_id='save_weather_to_csv',
    python_callable=save_weather_to_csv,
    dag=dag,
)

save_weather_to_csv_task