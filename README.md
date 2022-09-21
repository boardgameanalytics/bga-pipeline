# BGA ETL Pipeline

![flake8](https://github.com/boardgameanalytics/bga-pipeline/actions/workflows/flake8.yml/badge.svg?event=push)
![pytest](https://github.com/boardgameanalytics/bga-pipeline/actions/workflows/pytest.yml/badge.svg?event=push)

A fully automated ETL pipeline using Apache Airflow, BeautifulSoup4, and Pandas to create a data warehouse of board game data from [BoardGameGeek.com](https://boardgamegeek.com/) using their [BGGXMLAPI2](https://boardgamegeek.com/wiki/page/BGG_XML_API2).

This pipeline was created to prepare and deliver data for modeling and analysis in the [Boardgame Project Dashboard](https://github.com/boardgameanalytics/bga-web-dashboard).

# Contents
- [How to use this pipeline](#how-to-use)
  - [Docker Compose](#docker-compose)
  - [Airflow Web UI](#airflow-web-ui)
- [Customizations](#customizations)


# How to Use

## Clone repo
Clone this repo to where you want the Docker Environment to run out of:

```bash
git clone git@github.com:randynobx/boardgamegeek_pipeline.git
```

## Create .env
Create a `.env` file in the project directory and add your BGG login credentials
(for getting game ids) as:

```
BGG_USERNAME="your_username"
BGG_PASSWORD="password1234!"
```

## Setup Docker Environment
Build the custom `bgg-airflow` docker image:
```
make build
```

Initialize airflow and the `data` directory
```
make init
```

Start the full docker environment
```
make up
```
You should now be able to access the Airflow webserver at `http://localhost:8080` and continue configuration there.


## Finalize Configuration in Airflow Web UI

Using the Airflow Web UI, the following variables and connections need to be added for the DAG to work properly.

### `Admin`->`Variables`
Verify that the variables defined in `airflow_variables.json` are loaded.

### `Admin`->`Connections`
- Verify that the `api_bggxmlapi2` connection is present.

- Add connection for postgres database with the following:\
  `conn_id`   = postgres_db\
  `conn_type` = postgres\
  and your `host`/`login`/`password` info


# Customizations

## Airflow Configuration
Airflow will import connections and variables from the json files in `configs/`
when the `configs/setup_airflow.sh` script is run during the `make up` command.

You may modify existing connections/variables, or add new ones in these files:

- `airflow_connections.json`
- `airflow_variables.json`

*WARNING: Changing existing variable or connection entries may cause unexpected behavior!*
