"""Load functions for ETL pipeline"""

import re
from os import listdir
import pandas as pd
from sqlalchemy import create_engine

def main(csv_dir: str, conn_str: str) -> None:
    """Load csv files as tables in database

    Args:
        csv_dir (str): Path to directory containing csv files
        conn_str (str): Connection URI for SQL Alchemy
    """
    conn_str = re.sub(r'postgres://', 'postgresql://', conn_str)
    engine = create_engine(conn_str)
    # Load csv filenames
    csv_filenames = [file for file in listdir(csv_dir) if file[-4:] == '.csv']
    # Sort csv files by length to ensure relation tables are loaded last
    csv_filenames.sort(key=len)

    for filename in csv_filenames:
        filepath = f'{csv_dir}/{filename}'
        tablename = filename.split('.')[0]
        table_df = pd.read_csv(filepath, header=0)
        table_df.to_sql(tablename, engine, if_exists='append', index=None)
