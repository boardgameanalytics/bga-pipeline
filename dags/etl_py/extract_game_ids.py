"""Extract game IDs for all ranked games on BoardGameGeek.com"""

import re
from time import sleep
import requests
from dotenv import dotenv_values

def extract_game_ids(text: str) -> list:
    '''Extract game id's from webpage

    Args:
        text (str): text to extract game ids from

    Returns:
        list of game id's
    '''
    search_pattern = r'/boardgame/(\d+)/'
    # Change to set to remove duplicates
    return list(set(re.findall(search_pattern, text)))


def authenticate(username: str, password: str) -> requests.Session:
    """_summary_

    Args:
        username (str): bgg username
        password (str): bgg password

    Returns:
        requests.Session: authenticated requests session
    """
    login_url = 'https://boardgamegeek.com/login/api/v1'
    creds = {
    "credentials" : {
        "username" : username,
        "password" : password
        }
    }

    session = requests.Session()
    res = session.post(login_url, json=creds)
    if res.status_code == 204:
        return session
    raise Exception(f'Authentication unsuccessful. Status code {res.status_code} returned.')


def scrape_ranked_game_ids() -> list:
    """Extract game ids of all ranked games on BGG

    Returns:
        list: list of game ids as integers
    """
    # Create authenticated session
    creds = dotenv_values('.env')
    username, password = creds['BGG_USERNAME'], creds['BGG_PASSWORD']
    session = authenticate(username, password)

    # Instantiate list of game ids
    id_list = []

    # Iterate through browse pages 1+ until no more ids are returned
    page_num = 0
    while True:
        page_num += 1
        url = f'https://boardgamegeek.com/browse/boardgame/page/{page_num}?sort=rank&sortdir=asc'

        res = session.get(url)
        # Check that page was loaded successfully
        if res.status_code == 200:
            # Check that game ids were found on page
            if new_ids := extract_game_ids(res.content.decode()):
                # Add new ids to running list
                id_list.extend(new_ids)
                sleep(5) # Wait time between pages to reduce server strain
                continue # Continue to the next page

        # Conclude collection and return list of accumilated ids
        print(f'Finished on page {page_num}. Collected {len(id_list)} game ids.')
        return '\n'.join(list(set(id_list)))


def main(dest: str) -> None:
    """Run scraper and save to csv

    Args:
        dest (str): file to write output to
    """
    out = scrape_ranked_game_ids()
    with open(dest, 'w', encoding='utf-8') as file:
        file.write(out)
