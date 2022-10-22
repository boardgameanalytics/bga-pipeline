"""Extract game IDs for all ranked games on BoardGameGeek.com"""

import re
from os import getenv
from time import sleep
from pathlib import Path
from typing import Generator, List
from requests import Session
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def authenticate() -> Session:
    """Create authenticated Requests session with BGG.com"""
    load_dotenv()
    login_url = 'https://boardgamegeek.com/login/api/v1'
    creds = {
        "credentials": {
            "username": getenv('BGG_USERNAME'),
            "password": getenv('BGG_PASSWORD')
            }
    }

    session = Session()
    res = session.post(login_url, json=creds)
    if res.status_code == 204:
        return session
    raise Exception(f'Authentication unsuccessful. Status code {res.status_code} returned.')


def extract_ranked_game_ids(text: str) -> list:
    """Extract game id's from webpage

    Takes a BGG browse games html page as a string, and extracts game ids from
    all rows that have a numerical ranking. Non-ranked games have a ranking of
    'N/A' and will not be included in the returned list.

    Args:
        text (str): HTML as string to extract game ids from

    Returns:
        list of game id's
    """
    soup = BeautifulSoup(text, features='html.parser')
    id_list = []

    for row in soup.find_all(id="row_"):
        # if rank := row.find(class_='collection_rank'):
        rank = row.find(class_='collection_rank')
        if rank is not None:
            if rank.a:
                text = row.find(class_='primary').attrs['href']
                id_list.append(re.search(r'/boardgame/(\d+)/', text).group(1))

    return id_list


def scrape_browse_pages(max_pages: int, wait_time: int = 5) -> Generator[List[str], None, None]:
    """Extract game ids of all ranked games on BGG

    Returns:
        list: list of game ids as integers
    """

    print('Authenticating...')
    session = authenticate()
    print('Authentication Successful.')

    print('Beginning scrape...')
    for page_num in range(1, max_pages):
        url = f'https://boardgamegeek.com/browse/boardgame/page/{page_num}?sort=rank&sortdir=asc'

        res = session.get(url)
        if res.status_code == 200:
            # if new_ids := extract_ranked_game_ids(res.content.decode()):
            new_ids = extract_ranked_game_ids(res.content.decode())
            if new_ids is not None:
                print(page_num, end='')
                yield new_ids
                sleep(wait_time)
                continue

        print(f'\nFinished on page {page_num}.')
        break


def main(destination_path: Path, max_pages: int = 250) -> None:
    """Run scraper and save output to csv

    Args:
        destination_path (Path): file to write output to
        max_pages (int): Max number of pages to parse
    """
    with open(destination_path, 'w', encoding='utf-8') as file:
        for id_list in scrape_browse_pages(max_pages=max_pages):
            file.writelines([str(line) + "\n" for line in id_list])
