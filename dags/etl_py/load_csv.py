"""Load csv files into database"""

from os import listdir
import pandas as pd
from sqlalchemy import create_engine

def to_table(filepath, table, pg_conn_string):
    """
    Loads a pandas DataFrame to a bit.io database.
    Parameters
    ----------
    df : pandas.DataFrame
    destination : str
        Fully qualified bit.io PostgreSQL table name.
    pg_conn_string : str
        A bit.io PostgreSQL connection string including credentials.
    """
    # Validation and setup
    if pg_conn_string is None:
        raise ValueError("You must specify a PG connection string.")
    engine = create_engine(pg_conn_string)

    df = pd.read_csv(filepath, header=0)

    df.to_sql(
        table,
        engine,
        if_exists='append',
        index=False,
    )

def load_tables(csv_dir: str, conn_str: str):
    """Load all csv files to tables

    Args:
        csv_dir (str): _description_
        pg_conn_string (_type_): _description_
    """
    csv_filenames = [file for file in listdir(csv_dir) if file[-4:] == '.csv']

    # Sort by length to ensure relation tables are loaded last
    csv_filenames.sort(key=len)

    for filename in csv_filenames:
        if filename == 'game_description.csv':
            continue # Skip loading game_description
        filepath = f'{csv_dir}/{filename}'
        tablename = filename.split('.')[0]
        to_table(filepath, tablename, conn_str)
