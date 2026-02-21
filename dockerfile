FROM apache/airflow:2.10.1-python3.8

USER airflow

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

COPY dags/ /opt/airflow/dags/

USER root
RUN mkdir -p /opt/airflow/results
RUN chown -R airflow:root /opt/airflow/results

USER airflow

ENTRYPOINT ["airflow", "standalone"]