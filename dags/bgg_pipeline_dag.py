'''Boardgame ETL DAG'''

import sys
from pathlib import Path
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.models.baseoperator import chain
from airflow.operators.python import PythonOperator
from airflow.operators.sql import SQLValueCheckOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

sys.path.append("/opt/airflow/dag/py")
from py import extract_game_ids, extract_xml, transform_xml, load

# Grab current date
current_date = datetime.today().strftime('%Y-%m-%d')

# Default settings for all the dags in the pipeline
default_args = {

    "owner": "airflow",
    "start_date" : current_date,
    "retries" : 1,
    "retry_delay" : timedelta(minutes=5),
    "description" : "Automated ETL pipeline for extracting BGG.com data using \
        the BGGXMLAPI2 REST API."
}


DB_CONN_ID = Variable.get('db_conn_id')
BATCH_SIZE = int(Variable.get('batch_size'))
XML_DIR = Path(Variable.get('xml_dir'))
CSV_DIR = Path(Variable.get('csv_dir'))
GAME_IDS_FILE = Path(Variable.get('game_ids_file'))

def _count_rows(file: Path) -> int:
    """Get line count of file"""
    count = -1 # initialize to -1
    for count, _ in enumerate(file.open()):
        pass
    return count


with DAG(dag_id='bgg_pipeline',
         default_args=default_args,
         schedule_interval='00 4 * * *',
         catchup=False
         ) as dag:

    # Setup
    pg_hook = PostgresHook(postgres_conn_id=DB_CONN_ID)
    pg_engine = pg_hook.get_sqlalchemy_engine()

    # Check if the API is available
    is_api_available = HttpSensor(
        task_id='is_api_available',
        method='GET',
        http_conn_id='api_bggxmlapi2',
        endpoint='thing',
        request_params={'id':'50'},
        response_check= lambda response: 'item' in response.text,
        poke_interval = 5
    )

    # Extract game IDs
    extract_game_ids = PythonOperator(
        task_id='extract_game_ids',
        python_callable=extract_game_ids.main,
        op_kwargs={
            'dest': GAME_IDS_FILE
        }
    )

    # Extract
    extract_data = PythonOperator(
        task_id='extract_game_data',
        python_callable=extract_xml.main,
        op_kwargs={
            'game_ids_file': GAME_IDS_FILE,
            'dest_dir': XML_DIR,
            'batch_size': BATCH_SIZE
        }
    )

    # Transform
    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_xml.main,
        op_kwargs={
            'xml_dir': XML_DIR,
            'csv_dir': CSV_DIR
        }
    )

    # Create fresh staging tables
    create_staging_tables = PostgresOperator(
        task_id='create_staging_tables',
        postgres_conn_id=DB_CONN_ID,
        sql='sql/create_tables.sql'
    )

    # Load tables
    load_tables = PythonOperator(
        task_id='load_tables',
        python_callable=load.main,
        op_kwargs={
            'csv_dir': CSV_DIR,
            'engine': pg_engine
        }
    )

    csv_files = sorted([str(i) for i in CSV_DIR.iterdir()], key=len)
    validate_tables = []
    for path in csv_files:
        path = Path(path)
        tablename = path.stem
        row_count = _count_rows(path)
        # Validate table data
        validate_tables.append(SQLValueCheckOperator(
            task_id=f'validate_table_{tablename}',
            conn_id=DB_CONN_ID,
            sql=f"SELECT COUNT(*) FROM {tablename}",
            pass_value=row_count
        ))

    # Dependencies
    chain(
        is_api_available,
        extract_game_ids,
        extract_data,
        transform_data,
        create_staging_tables,
        load_tables,
        validate_tables
    )
