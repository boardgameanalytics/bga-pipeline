from pathlib import Path
from requests import Session
from dags.py.extract_game_ids import authenticate
from dags.py.extract_game_ids import scrape_browse_pages
from dags.py.extract_game_ids import extract_ranked_game_ids
from dags.py.extract_game_ids import main


def test_authenticate():
    assert isinstance(authenticate(), Session)


def test_extract_ranked_game_ids():
    with open('tests/assets/test_browse_page.html', 'r') as file:
        test_html = file.read()
    id_list = extract_ranked_game_ids(test_html)
    assert all(map(str.isnumeric, id_list))


def test_scrape_browse_pages():
    id_list = list(scrape_browse_pages(2))[0]
    print(id_list)
    assert all(map(str.isnumeric, id_list))


def test_main():
    test_csv = Path('tests/assets/tmp_game_ids.csv')
    test_csv.unlink(missing_ok=True)
    main(destination_path=test_csv, max_pages=2)
    assert test_csv.exists(), 'game-id file was not created'
    with open(test_csv, 'r') as file:
        id_list = file.read().split('\n')
    assert all(map(str.isnumeric, id_list[:-1])), 'Unexpected content found in game-id file'
    test_csv.unlink()
