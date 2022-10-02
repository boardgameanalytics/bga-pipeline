"""ETL Pipeline for game batch XML -> csv"""

import re
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup

CLASS_TYPES = ['mechanic', 'category', 'designer', 'artist', 'publisher']


def transform_game_data(game_soup: BeautifulSoup) -> pd.DataFrame:
    """Transform game data from XML fragment to Pandas DataFrame

    Args:
        game_soup (BeautifulSoup): Game data as BeautifulSoup object

    Returns:
        pd.DataFrame: Game data as Pandas DataFrame
    """
    raw = {
        'id': [int(game_soup.attrs['id'])],
        'title': [game_soup.find('name').attrs['value']],
        'release_year': [int(game_soup.yearpublished.attrs['value'])],
        'avg_rating': [float(game_soup.find('average').attrs['value'])],
        'bayes_rating': [float(game_soup.find('bayesaverage').attrs['value'])],
        'total_ratings': [int(game_soup.find('usersrated').attrs['value'])],
        'std_ratings': [float(game_soup.find('stddev').attrs['value'])],
        'min_players': [int(game_soup.minplayers.attrs['value'])],
        'max_players': [int(game_soup.maxplayers.attrs['value'])],
        'min_playtime': [int(game_soup.minplaytime.attrs['value'])],
        'max_playtime': [int(game_soup.maxplaytime.attrs['value'])],
        'min_age': [int(game_soup.find('minage').attrs['value'])],
        'weight': [float(game_soup.find('averageweight').attrs['value'])],
        'owned_copies': [int(game_soup.find('owned').attrs['value'])],
        'wishlist': [int(game_soup.find('wishing').attrs['value'])],
        'kickstarter': [bool(game_soup.find('link', id='8374'))]
    }

    return pd.DataFrame.from_dict(raw)


def transform_game_description(game_soup: BeautifulSoup) -> pd.DataFrame:
    """Transform game descriptions to Pandas DataFrame

    Args:
        game_soup (BeautifulSoup): Game data as BeautifulSoup object

    Returns:
        pd.DataFrame: Game description as Pandas DataFrame
    """
    desc = str(game_soup.find('description').string)
    desc = re.sub(r'&rsquo;', '\'', desc)
    desc = re.sub(r'&#.{,5};', ' ', desc)
    desc = re.sub(r' {2,}', ' ', desc)
    desc = desc.strip()

    raw = {
        'game_id': [int(game_soup.attrs['id'])],
        'description': [desc]
    }

    return pd.DataFrame.from_dict(raw)


def transform_game_classification(name: str, game_soup: BeautifulSoup) -> pd.DataFrame:
    """Transform given classification ids from game's XML fragment to Pandas DataFrame

    Args:
        name (str): Classification to extract from data
        game_soup (BeautifulSoup): Game data as BeautifulSoup object

    Returns:
        pd.DataFrame: Game classification data as Pandas DataFrame
    """
    raw = [(int(line.attrs['id']), str(line.attrs['value']))
           for line in game_soup.find_all('link', type=f'boardgame{name}')]

    return pd.DataFrame.from_records(raw, columns=['id', 'name'])


def transform_class_map(name: str, game_soup: BeautifulSoup) -> pd.DataFrame:
    """Create mapping of game classifications

    Args:
        name (str): Classification to create map of
        game_soup (BeautifulSoup): Game data as BeautifulSoup object

    Returns:
        pd.DataFrame: Relationship table as Pandas DataFrame
    """
    raw = [(int(game_soup.attrs['id']), int(line.attrs['id']))
           for line in game_soup.find_all('link', type=f'boardgame{name}')]
    return pd.DataFrame.from_records(raw, columns=['game_id', f'{name}_id'])


def save_df(dataframe: pd.DataFrame, destination_path: Path) -> None:
    """Save DataFrame to csv file"""
    with open(destination_path, 'w', encoding='utf-8') as file:
        dataframe.to_csv(file, index=False)


def main(xml_dir: Path, csv_dir: Path) -> None:
    """Transform XML game data to CSV files"""
    games = []
    game_desc = []
    classifications = {item: [] for item in CLASS_TYPES}
    class_maps = {item: [] for item in CLASS_TYPES}

    for xml_file in xml_dir.glob('*.xml'):

        with xml_file.open() as file:
            batch = BeautifulSoup(file, features='xml')

        for game_soup in batch.items.children:
            if game_soup != '\n':
                games.append(transform_game_data(game_soup))
                game_desc.append(transform_game_description(game_soup))
                for name, data in classifications.items():
                    data.append(transform_game_classification(name, game_soup))
                for name, data in class_maps.items():
                    data.append(transform_class_map(name, game_soup))

    save_df(pd.concat(games).drop_duplicates(), csv_dir / 'game.csv')
    save_df(pd.concat(game_desc).drop_duplicates(), csv_dir / 'game_description.csv')

    for name, dfs in classifications.items():
        save_df(pd.concat(dfs).drop_duplicates(), csv_dir / f'{name}.csv')

    for name, dfs in class_maps.items():
        save_df(pd.concat(dfs).drop_duplicates(), csv_dir / f'game_{name}.csv')
