from pathlib import Path
import sqlite3
import pandas as pd
from dags.py_modules.load import load_table


def test_load_table():
    csv_path = Path('tests/assets/test_table.csv')
    db_path = Path('tests/assets/test.db')

    csv_df = pd.read_csv(csv_path)
    db_path.unlink(missing_ok=True)

    with sqlite3.connect(db_path) as db_conn:
        load_table(csv_path=csv_path, engine=db_conn)

        db_df = pd.read_sql_query("SELECT * FROM test_table", db_conn)
        assert len(csv_df.compare(db_df)) == 0

    db_path.unlink()
