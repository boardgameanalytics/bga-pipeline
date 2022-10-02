from requests import Session
from dags.py.extract_game_ids import authenticate
from dags.py.extract_game_ids import extract_ranked_game_ids


def test_authenticate():
    assert isinstance(authenticate(), Session)


def test_extract_ranked_game_ids():
    raise NotImplementedError


def test_scrape_browse_pages():
    raise NotImplementedError
