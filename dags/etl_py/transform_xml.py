'''ETL Pipeline for game batch XML -> csv'''

import re
from os import listdir
import pandas as pd
from bs4 import BeautifulSoup


def transform_game_data(game_soup: BeautifulSoup) -> pd.DataFrame:
    '''Transform game data from XML fragment to dict'''
    
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
        'weight': [float(game_soup.find('averageweight').attrs['value'])],
        'owned_copies': [int(game_soup.find('owned').attrs['value'])]
    }

    return pd.DataFrame.from_dict(raw)

def transform_game_desc(game_soup: BeautifulSoup) -> pd.DataFrame:
    raw = {
        'game_id': [int(game_soup.attrs['id'])],
        'description': [str(game_soup.find('description').string)]
    }
    
    return pd.DataFrame.from_dict(raw)

def transform_game_classification(name: str, game_soup: BeautifulSoup) -> pd.DataFrame:
    '''Transform given classification ids from game's XML fragment to list'''
    
    raw = [(int(line.attrs['id']), str(line.attrs['value']))
            for line in game_soup.find_all('link', type=f'boardgame{name}')]

    return pd.DataFrame.from_records(raw, columns=['id', 'name'])


def transform_class_map(name: str, game_soup: BeautifulSoup) -> pd.DataFrame:
    '''Create mapping of game classifications'''
    raw = [(int(game_soup.attrs['id']), int(line.attrs['id']))
            for line in game_soup.find_all('link', type=f'boardgame{name}')]
    return pd.DataFrame.from_records(raw, columns=['game_id', f'{name}_id'])


def save_df(dataframe: pd.DataFrame, name: str, csv_dir: str) -> None:
    '''Consolidate list and save df to csv'''
    with open(f'{csv_dir}/{name}.csv', 'w', encoding='utf-8') as file:
        dataframe.drop_duplicates().to_csv(file, index=False)


def main(xml_dir: str, csv_dir: str):
    '''Create DataFrames'''
    class_types = ['mechanic', 'category', 'designer', 'artist', 'publisher']

    # Instantiate lists of records for each table
    games = []
    game_desc = []
    classifications = {item: [] for item in class_types}
    class_maps = {item: [] for item in class_types}

    # Get list of all xml files in xml_dir
    xml_files = [file for file in listdir(xml_dir) if file[-4:] == '.xml']


    ## Transform xml to pandas dataframe ##
    
    # Iterate through all xml batch files
    for filename in xml_files:
        # Load xml file
        filepath = f'{xml_dir}/{filename}'
        with open(filepath, 'rb') as file:
            batch = BeautifulSoup(file, features='xml')

        # Split xml file into list of individual games
        game_batch = [item for item in batch.items.children if item != '\n']

        # Iterate through each game node
        for game_soup in game_batch:
            games.append(transform_game_data(game_soup))
            game_desc.append(transform_game_desc(game_soup))
            for name, data in classifications.items():
                data.append(transform_game_classification(name, game_soup))
            for name, data in class_maps.items():
                data.append(transform_class_map(name, game_soup))


    ## Merge dataframes ##
    
    games = pd.concat(games)
    game_desc = pd.concat(game_desc)
    
    # classification data
    for name, dfs in classifications.items():
        classifications['name'] = pd.concat(dfs)

    # game-classification relationships
    for name, dfs in class_maps.items():
        classifications['name'] = pd.concat(dfs)


    ## Data cleaning ##
    def clean_description(text: str):
        text = re.sub(r'&rsquo;', '\'', text)
        text = re.sub(r'&#.{,5};', ' ', text)
        text = re.sub(r' {2,}', ' ', text)
        return text.strip()
    game_desc['description'].apply(clean_description)


    ## Save to csv ##
    save_df(games, 'game', csv_dir)
    save_df(game_desc, 'game_description', csv_dir)

    # classification data
    for name, df in classifications.items():
        save_df(df, name, csv_dir)

    # game-classification relationships
    for name, df in class_maps.items():
        save_df(df, f'game_{name}', csv_dir)
