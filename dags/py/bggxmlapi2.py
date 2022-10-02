"""Helper functions for using the BGGXMLAPI2"""

import requests


def build_query(query_type: str, params: dict) -> str:
    """Build XML query for board game

    Args:
        query_type (str): type of query: thing, user, search...
        params (dict): dict of params using str for both keys and values

    Returns:
        str: Query URL for given parameters
    """
    url = f'https://boardgamegeek.com/xmlapi2/{query_type}?'
    return url + '&'.join([f'{key}={str(value)}' for key, value in params.items()])


def fetch_game(game_id: str) -> str:
    """Fetch game data from BGG

    Args:
        game_id (str): numerical id of game on BGG

    Returns:
        str: Game data encoded with XML
    """
    params = {
        'stats': '1',
        'id': game_id
    }
    request_url = build_query('thing', params)
    return requests.get(url=request_url).content.decode()
