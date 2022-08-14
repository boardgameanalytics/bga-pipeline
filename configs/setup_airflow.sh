#!/usr/bin/env bash

# Clear existing api connection
airflow connections delete api_bggxmlapi2

# Import connection and variable files
airflow connections import /opt/airflow/configs/airflow_connections.json
airflow variables import /opt/airflow/configs/airflow_variables.json
