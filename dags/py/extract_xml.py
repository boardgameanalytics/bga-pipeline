"""Scrape game information from BGG

Takes bgg game ids and generates batched xml files
"""

from pathlib import Path
from math import ceil
from typing import Generator
from .bggxmlapi2 import fetch_game


def save_file(path: Path, content: str) -> bool:
    """Save page to file"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
    return path.exists()


def scrape_game_pages(game_ids_list: list, batch_size: int) -> Generator[str, None, None]:
    """Fetch, save, and extract data from game pages

    Args:
        game_ids_list (list): list of game ids to scrape
        batch_size (int): number of ids to bundle into each request

    Returns:
        Yields batches of games as Response objects
    """
    total_batches = ceil(len(game_ids_list) // batch_size) + 1
    for batch_num in range(total_batches):
        begin = batch_num * batch_size
        end = min(begin + batch_size, len(game_ids_list))
        id_batch = ','.join(game_ids_list[begin:end])
        yield fetch_game(id_batch)


def main(game_ids_file: Path, destination_dir: Path, batch_size: int) -> None:
    """Run scraper

    Args:
        game_ids_file (Path): Filepath of csv file containing game id's
        destination_dir (Path): Filepath of directory to save xml files
        batch_size (int): Number of games to include per API query
    """
    with game_ids_file.open() as file:
        game_ids = file.read().split('\n')

    for num, xml in enumerate(scrape_game_pages(game_ids, batch_size)):
        destination_path = destination_dir / f'bgg_games_batch_{str(num).zfill(2)}.xml'
        save_file(destination_path, xml)
