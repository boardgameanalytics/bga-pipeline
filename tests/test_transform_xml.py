from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
from dags.py_modules.transform_xml import transform_game_data
from dags.py_modules.transform_xml import transform_game_description
from dags.py_modules.transform_xml import transform_game_classification
from dags.py_modules.transform_xml import transform_class_map
from dags.py_modules.transform_xml import save_df
from dags.py_modules.transform_xml import main


def _setup_soup():
    with open(Path('tests/assets/test_xml.xml'), 'r') as file:
        test_xml = file.read()
    return BeautifulSoup(test_xml, features='xml')


def test_transform_game_data():
    xml = _setup_soup()
    df = transform_game_data(game_soup=xml.items.item)
    assert df.shape == (1, 16)


def test_transform_game_description():
    xml = _setup_soup()
    df = transform_game_description(game_soup=xml.items.item)
    assert df.shape == (1, 2)


def test_transform_game_classification():
    xml = _setup_soup()
    df = transform_game_classification('mechanic', game_soup=xml.items.item)
    assert df.shape == (8, 2)


def test_transform_class_map():
    xml = _setup_soup()
    df = transform_class_map('designer', game_soup=xml.items.item)
    assert df.shape == (3, 2)


def test_save_df():
    tmp_df = pd.DataFrame({'id': [0, 1], 'col': ['test', 'test2']})
    tmp_file = Path('tests/assets/tmp_file.csv')
    tmp_file.unlink(missing_ok=True)

    save_df(tmp_df, tmp_file)

    assert tmp_file.exists(), 'File was not created'
    saved_df = pd.read_csv(tmp_file)
    assert len(tmp_df.compare(saved_df)) == 0, 'Unexpected data found in file'

    tmp_file.unlink()


def test_main():
    xml_dir = Path('tests/assets')
    csv_dir = Path('tests/assets/tmp_dir_t')
    if not csv_dir.exists():
        csv_dir.mkdir()
    for file in csv_dir.iterdir():
        file.unlink()

    main(xml_dir=xml_dir, csv_dir=csv_dir)
    for csv in csv_dir.glob(r'*.csv'):
        df = pd.read_csv(csv)
        assert df.shape[1] > 0
        csv.unlink()
    csv_dir.rmdir()
