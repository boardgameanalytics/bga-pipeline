'''Scrape game ids'''

from datetime import date
from io import StringIO
import requests
import pandas as pd

def main(dest: str):
    """Extract and save game ids

    Args:
        dest (str): Save ids to dest file
    """

    # Extract from @beefsack's historical rankings repo
    file_date = date.today().strftime("%Y-%m-%d") # YYYY-MM-DD
    file_date = "2022-08-13" # Last known good file
    url = f'https://raw.githubusercontent.com/beefsack/bgg-ranking-historicals/master/{file_date}.csv'

    # Fetch latest rankings from github
    res = requests.get(url)

    # Prep data for pandas
    raw_data = StringIO(res.content.decode('utf-8'))

    # Load raw data into DataFrame
    raw_df = pd.read_csv(raw_data, header=0, sep=',')

    # Save IDs to file
    raw_df['ID'].to_csv(dest, header=None, index=None)
