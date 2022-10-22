from pathlib import Path
from bs4 import BeautifulSoup
from requests import Response
from dags.py_modules.extract_xml import save_file
from dags.py_modules.extract_xml import scrape_game_pages
from dags.py_modules.extract_xml import main


def test_save_file() -> None:
    text = "This is a test file."
    tmp_file = Path('tmp_file.txt')
    tmp_file.unlink(missing_ok=True)

    assert save_file(tmp_file, text)
    assert tmp_file.exists(), 'File not created'

    tmp_file.unlink()


def test_save_file_missing_dir() -> None:
    text = "This is a test file."
    tmp_file = Path('test_assets/tmp_file.txt')

    tmp_file.unlink(missing_ok=True)
    if tmp_file.parent.exists():
        tmp_file.parent.rmdir()

    assert save_file(tmp_file, text)
    assert tmp_file.exists(), 'File not created'

    tmp_file.unlink()
    tmp_file.parent.rmdir()


def test_scrape_game_pages() -> None:
    game_ids = ['187645', '220308']
    test_res = list(scrape_game_pages(game_ids, 2))[0]

    assert(isinstance(test_res, str)), 'Function did not return str object'
    soup = BeautifulSoup(test_res, features='xml')
    assert len([x for x in soup.items if x != '\n']) == 2


def test_main():
    tmp_dir = Path('tests/assets/tmp_dir')
    game_ids_path = Path('tests/assets/test_game_ids.csv')

    main(game_ids_file=game_ids_path,
         destination_dir=tmp_dir,
         batch_size=50)

    saved_files = list(tmp_dir.glob(r'*.xml'))
    print(saved_files)
    assert len(saved_files) == 3
    for file in saved_files:
        file.unlink()
    tmp_dir.rmdir()
