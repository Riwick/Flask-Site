import os.path

from dotenv import load_dotenv

dotenv_path = os.path.exists("src/.env")

if dotenv_path:
    load_dotenv("src/.env")


SECRET_KEY = os.environ.get("SECRET_KEY")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
