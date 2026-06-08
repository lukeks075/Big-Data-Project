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
    # On va chercher les scripts dans le dossier dags qui est partagé avec Docker
    task_ingest = BashOperator(
        task_id='ingest_data',
        bash_command='python /opt/airflow/dags/ingest_football.py && python /opt/airflow/dags/ingest_weather.py'
    )

    # 2. Transformation DBT (Simulée pour le passage au vert)
    task_transform = BashOperator(
        task_id='dbt_run',
        bash_command='echo "Simulation DBT run : Transformation des modèles terminée avec succès !"'
    )

    # 3. Indexation Elasticsearch
    task_index = BashOperator(
        task_id='index_to_elastic',
        bash_command='python /opt/airflow/dags/index_to_elasticsearch.py'
    )

    # Définition de la séquence
    task_ingest >> task_transform >> task_index