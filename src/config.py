import os.path

from dotenv import load_dotenv

dotenv_path = os.path.exists("src/.env")

if dotenv_path:
    load_dotenv("src/.env")


SECRET_KEY = os.environ.get("SECRET_KEY")
