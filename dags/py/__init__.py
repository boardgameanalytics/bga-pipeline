from pathlib import Path
from dotenv import load_dotenv

dotenv = Path('.env')
if dotenv.exists():
    load_dotenv('.env')
