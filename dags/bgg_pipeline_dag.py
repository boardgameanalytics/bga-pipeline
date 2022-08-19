'''Boardgame ETL DAG'''

import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.models.baseoperator import chain
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python import PythonOperator
from airflow.operators.sql import SQLCheckOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator

sys.path.append("/opt/airflow/dag/etl_py")
from etl_py import extract_game_ids, extract_xml, transform_xml, load

# Grab current date
current_date = datetime.today().strftime('%Y-%m-%d')

# Default settings for all the dags in the pipeline
default_args = {

    "owner": "Airflow",
    "start_date" : current_date,
    "retries" : 1,
    "retry_delay": timedelta(minutes=5)

}


DB_CONN_ID = Variable.get('db_conn_id') # 'postgres_db'
BATCH_SIZE = int(Variable.get('batch_size')) # 1200
XML_PATH = Variable.get('xml_path') # 'data/xml'
CSV_PATH = Variable.get('csv_path') # 'data/csv'
GAME_IDS_FILE = Variable.get('game_ids_file') # 'data/game_ids.csv'


with DAG('bgg_pipeline',
         default_args=default_args,
         schedule_interval='00 5 * * *',
         catchup=False
         ) as dag:

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
            'dest_path': XML_PATH,
            'batch_size': BATCH_SIZE
        }
    )

    # Transform
    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_xml.main,
        op_kwargs={
            'xml_dir': XML_PATH,
            'csv_dir': CSV_PATH
        }
    )

    # Create fresh staging tables
    create_staging_tables = PostgresOperator(
        task_id = 'create_staging_tables',
        postgres_conn_id=DB_CONN_ID,
        sql='sql/create_tables.sql'
    )

    # Load data to db
    load_data = PythonOperator(
        task_id = 'load_data',
        python_callable=load.main,
        op_kwargs={
            'csv_dir': CSV_PATH,
            'conn_str': BaseHook.get_connection(DB_CONN_ID).get_uri()
        }
    )

    # Validate
    validate_table_game = SQLCheckOperator(
        task_id='validate_table_game',
        conn_id=DB_CONN_ID,
        sql='''
            SELECT COUNT(*) FROM game
        '''
    )

    # Dependencies
    chain(
        is_api_available,
        extract_ids,
        extract_data,
        transform_data,
        create_staging_tables,
        load_data,
        validate_table_game
    )
