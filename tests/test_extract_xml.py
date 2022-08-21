"""Unit tests for  extract_xml.py"""

from pathlib import Path
from dags.py.extract_xml import save_file

def test_save_file() -> None:
    """Test save function"""
    text = "This is a test file."
    testfile = Path('testfile.txt')

    testfile.unlink(missing_ok=True)

    save_file(testfile, text)

    assert testfile.exists(), 'File not created'

    testfile.unlink()


def test_save_file_missing_dir() -> None:
    """Test save function inside directory"""
    text = "This is a test file."
    testfile = Path('test_assets/testfile.txt')

    testfile.unlink(missing_ok=True)
    if testfile.parent.exists():
        testfile.parent.rmdir()

    save_file(testfile, text)

    assert testfile.exists(), 'File not created'

    testfile.unlink()
    testfile.parent.rmdir()

def test_scrape_game_pages() -> None:
    """Test scraping function"""
    pass
