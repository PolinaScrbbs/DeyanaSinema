from dotenv import load_dotenv
import os

os.environ.pop("DB_USER", None)
os.environ.pop("DB_PASSWORD", None)
os.environ.pop("DB_NAME", None)

os.environ.pop("DATABASE_URL", None)
os.environ.pop("SECRET_KEY", None)


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
