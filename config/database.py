from os import getenv, path
from dotenv import load_dotenv

from sqlalchemy import create_engine


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")

SQLALCHEMY_DATABASE_URI = f"mariadb+mariadbconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"


def connect_to_database(database):
    return create_engine(SQLALCHEMY_DATABASE_URI+database)
