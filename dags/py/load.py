"""Load functions for ETL pipeline"""

from pathlib import Path
import pandas as pd


def load_table(csv_path: Path, engine) -> None:
    """Load contents of CSV file into SQL database table

    Args:
        csv_path (str): Path of CSV file to load into table
        engine: DB connection object
    """
    table_name = csv_path.stem
    table_df = pd.read_csv(csv_path, header=0)
    table_df.to_sql(table_name, engine, if_exists='append', index=None)
