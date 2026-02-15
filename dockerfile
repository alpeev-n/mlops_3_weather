FROM apache/airflow:2.10.1-python3.8

USER root

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

RUN mkdir -p /opt/airflow/dataset
RUN chown -R airflow:root /opt/airflow/dataset

COPY dags/ /opt/airflow/dags/

USER airflow

ENTRYPOINT ["airflow", "standalone"]