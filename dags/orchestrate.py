from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
# from src.fetch_data import fetch_data
# from src.fetch_data import insert_crypto_data
from dotenv import load_dotenv
import os
import sys

# Dynamically add the parent directory (project root) to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fetch_data import fetch_data
from fetch_data import insert_crypto_data

default_args = {
    'owner': 'shiv',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

load_dotenv()

CURRENCY = "usd"
PER_PAGE = 250
API_KEY = os.getenv("API_KEY")

def fetch_crypto_data_task(**context):
    data = fetch_data(API_KEY, CURRENCY, PER_PAGE)
    context['ti'].xcom_push(key='crypto_data', value=data)

def insert_crypto_data_task(**context):
    data = context['ti'].xcom_pull(task_ids='fetch_crypto_data', key='crypto_data')
    insert_crypto_data(data)

with DAG(
    dag_id='crypto_data_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 5, 1),
    schedule='@daily',
    catchup=False,
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_crypto_data',
        python_callable=fetch_crypto_data_task,
        provide_context=True
    )

    insert_task = PythonOperator(
        task_id='insert_crypto_data',
        python_callable=insert_crypto_data_task,
        provide_context=True
    )

    fetch_task >> insert_task