from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from extractionscript import extract_dawn_data, extract_bbc_data

# Define default arguments for the DAG
default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 5, 12),  # Modify start date as needed
    'schedule_interval': '@daily'  # Modify schedule interval as needed
}

# Define the DAG
dag = DAG(
    'data_extraction_and_storage',
    default_args=default_args,
    description='DAG for data extraction, transformation, and storage',
    catchup=False
)

# Task 1: Data Extraction from Dawn.com
extract_dawn_task = PythonOperator(
    task_id='extract_dawn_data',
    python_callable=extract_dawn_data,
    dag=dag
)

# Task 2: Data Extraction from BBC.com
extract_bbc_task = PythonOperator(
    task_id='extract_bbc_data',
    python_callable=extract_bbc_data,
    dag=dag
)

# Task 3: Data Transformation (Already defined in extractionscript.py)

# Task 4: Data Storage (Already defined in extractionscript.py)

# Define task dependencies
extract_dawn_task >> extract_bbc_task
