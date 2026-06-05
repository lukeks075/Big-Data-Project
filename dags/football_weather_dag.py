from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Configuration du DAG
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'football_weather_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    # 1. Ingestion des données (Football & Weather)
    task_ingest = BashOperator(
        task_id='ingest_data',
        bash_command='python C:/Users/ldear/big-data-project/ingest_football.py && python C:/Users/ldear/big-data-project/ingest_weather.py'
    )

    # 2. Transformation DBT (Le cœur du calcul)
    task_transform = BashOperator(
        task_id='dbt_run',
        bash_command='dbt run --project-dir C:/Users/ldear/big-data-project/'
    )

    # 3. Indexation Elasticsearch
    task_index = BashOperator(
        task_id='index_to_elastic',
        bash_command='python C:/Users/ldear/big-data-project/index_to_elasticsearch.py'
    )

    # Définition de la séquence
    task_ingest >> task_transform >> task_index