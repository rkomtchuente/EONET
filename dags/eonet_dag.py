from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# ensures Airflow can find your ETL script
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Assuming you wrap your ETL script's logic in a function called run_etl() inside "natural events ETL.py"
from natural_events_ETL import eonet_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}
# Defines DAG workflow.
eonet_dag = DAG(
    'eonet_hourly',
    default_args=default_args,
    description='Run EONET ETL Hourly',
    schedule_interval=timedelta(hours=1),
    catchup=False,
    is_paused_upon_creation=False
)
# Defines task to be executed
run_eonet_etl_task = PythonOperator(
    task_id='run_eonet_etl',
    python_callable=eonet_etl,
    dag=eonet_dag,
)