from dotenv import load_dotenv
import os

os.environ.pop("DB_USER", None)
os.environ.pop("DB_PASSWORD", None)

os.environ.pop("DB_HOST", None)
os.environ.pop("DB_PORT", None)
os.environ.pop("DB_NAME", None)

os.environ.pop("SECRET_KEY", None)
os.environ.pop("DATABASE_URL", None)

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
