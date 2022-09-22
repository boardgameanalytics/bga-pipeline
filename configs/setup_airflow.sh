#!/usr/bin/env bash

# Clear existing and import API connection
airflow connections delete api_bggxmlapi2
airflow connections add 'api_bggxmlapi2' \
    --conn-type 'http' \
    --conn-host 'https://boardgamegeek.com/xmlapi2'

# Import connection and variable files
if [[ -f /opt/airflow/configs/airflow_connections.json ]]; then
    airflow connections import /opt/airflow/configs/airflow_connections.json
fi;
airflow variables import /opt/airflow/configs/airflow_variables.json
