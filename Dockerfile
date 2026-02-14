# Dockerfile
FROM apache/airflow:2.8.3-python3.11

# Устанавливаем системные зависимости (если нужны)
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Возвращаемся к пользователю airflow
USER airflow

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Добавление src в PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/src"