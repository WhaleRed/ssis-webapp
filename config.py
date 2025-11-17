from os import getenv
from dotenv import load_dotenv


load_dotenv()

DB_HOST = getenv("DB_HOST")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")
DB_PORT = getenv("DB_PORT")
SECRET_KEY = getenv("SECRET_KEY")
DB_URL = getenv("DB_URL")
DB_KEY = getenv("DB_KEY")