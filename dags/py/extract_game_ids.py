"""Extract game IDs for all ranked games on BoardGameGeek.com"""

import re
from time import sleep
import requests
from bs4 import BeautifulSoup
from dotenv import dotenv_values

# constraints
MAX_PAGE_NUM = 250
WAIT_TIME = 5 # seconds


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


def extract_ranked_game_ids(text: str) -> list:
    '''Extract game id's from webpage

    Takes a BGG browse games html page as a string, and extracts game ids from
    all rows that have a numerical ranking. Non ranked games have a ranking of
    'N/A' and will not be included in the returned list.

    Args:
        text (str): HTML as string to extract game ids from

    Returns:
        list of game id's
    '''
    soup = BeautifulSoup(text, features='html')
    def _extract(soup: BeautifulSoup):
        for row in soup.find_all(id="row_"):
            #if rank := row.find(class_='collection_rank'):
            rank = row.find(class_='collection_rank')
            if rank is not None:
                if rank.a:
                    text = row.find(class_='primary').attrs['href']
                    yield re.search(r'/boardgame/(\d+)/', text).group(1)

    return list(_extract(soup))


def scrape_browse_pages():
    """Extract game ids of all ranked games on BGG

    Returns:
        list: list of game ids as integers
    """

    # Create authenticated session
    print('Authenticating...', sep='')
    creds = dotenv_values('.env')
    username, password = creds['BGG_USERNAME'], creds['BGG_PASSWORD']
    session = authenticate(username, password)
    print('Successful. Beginning scrape...')

    # Iterate through browse pages 1+ until no more ids are returned
    for page_num in range(1, MAX_PAGE_NUM):
        url = f'https://boardgamegeek.com/browse/boardgame/page/{page_num}?sort=rank&sortdir=asc'

        res = session.get(url)
        # Check that page was loaded successfully
        if res.status_code == 200:
            # Check that game ids were found on page
            #if new_ids := extract_ranked_game_ids(res.content.decode()):
            new_ids = extract_ranked_game_ids(res.content.decode())
            if new_ids is not None:
                print(page_num, end='')
                yield new_ids # Yield list of current pages id
                sleep(WAIT_TIME) # Pause between pages to reduce request freq
                continue # Continue to the next page

        # Conclude collection and return list of accumilated ids
        print(f'\nFinished on page {page_num}.')
        break


def main(dest: str) -> None:
    """Run scraper and save to csv

    Args:
        dest (str): file to write output to
    """
    with open(dest, 'w', encoding='utf-8') as file:
        for id_list in scrape_browse_pages():
            file.writelines([str(line) + "\n" for line in id_list])
