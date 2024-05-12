from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from extractionscript import extract_dawn_data, extract_bbc_data, preprocess_dawn_data, preprocess_bbc_data, store_data_function

# Define default arguments for the DAG
default_args = {
    'owner': '20I-0923_Ghulam Muhammad',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 5, 12),  
    'schedule_interval': '@daily'  
}

# Define the DAG
dag = DAG(
    'data_extraction_preprocessing_storage',
    default_args=default_args,
    description='DAG for data extraction, preprocessing, and storage',
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

# Task 3: Data Preprocessing for Dawn.com
preprocess_dawn_task = PythonOperator(
    task_id='preprocess_dawn_data',
    python_callable=preprocess_dawn_data,
    provide_context=True,  
    dag=dag
)

# Task 4: Data Preprocessing for BBC.com
preprocess_bbc_task = PythonOperator(
    task_id='preprocess_bbc_data',
    python_callable=preprocess_bbc_data,
    provide_context=True,  
    dag=dag
)

# Task 5: Data Storage
store_data_task = PythonOperator(
    task_id='store_data',
    python_callable=store_data_function,  
    provide_context=True,  
    dag=dag
)

# Define task dependencies
extract_dawn_task >> preprocess_dawn_task >> store_data_task
extract_bbc_task >> preprocess_bbc_task >> store_data_task
