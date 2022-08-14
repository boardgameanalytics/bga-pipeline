"""Load csv files into database"""

from os import listdir
import pandas as pd
from sqlalchemy import create_engine

def to_table(filepath: str, table: str, db_conn_str: str) -> None:
    """Load csv file to sql table

    Args:
        filepath (str): csv file location
        table (str): Table name to save file to
        db_conn_str (str): DB connection URI string with credentials
    """
    # Validation and setup
    if db_conn_str is None:
        raise ValueError("You must specify a PG connection string.")
    engine = create_engine(db_conn_str)

    df = pd.read_csv(filepath, header=0)

    df.to_sql(
        table,
        engine,
        if_exists='append',
        index=False,
    )

def load_tables(csv_dir: str, db_conn_str: str) -> None:
    """Load all csv files to tables

    Args:
        csv_dir (str): Location directory containing csv files
        db_conn_str (str): DB connection URI string with credentials
    """
    csv_filenames = [file for file in listdir(csv_dir) if file[-4:] == '.csv']

    # Sort by length to ensure relation tables are loaded last
    csv_filenames.sort(key=len)

    for filename in csv_filenames:
        if filename == 'game_description.csv':
            continue # Skip loading game_description
        filepath = f'{csv_dir}/{filename}'
        tablename = filename.split('.')[0]
        to_table(filepath, tablename, db_conn_str)
