build:
	docker compose build

init: build clean-data
	docker compose --project-name bgg-airflow up airflow-init

up:
	docker compose --project-name bgg-airflow up --detach
	docker exec bgg-airflow-airflow-webserver-1 /bin/bash /opt/airflow/configs/setup_airflow.sh

down:
	docker compose --project-name bgg-airflow down

clean-docker:
	docker compose --project-name bgg-airflow down --volumes --rmi all 

clean-data:
	rm -rf data
	mkdir -p data/csv
	mkdir -p data/xml

reset: clean-docker init up