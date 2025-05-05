FROM apache/airflow:3.0.0
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} --no-cache-dir -r requirements.txt
