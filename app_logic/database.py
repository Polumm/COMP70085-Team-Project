import configparser
from adbc_driver_postgresql.dbapi import connect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timezone

# from app_logic.models import PlayerScore


# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()


def init_db_connection(db_url):
    """
    Initialize a database connection using a given URL.
    :param db_url: The database connection URL.
    :return: A connection and cursor object.
    """
    conn = connect(db_url)
    cur = conn.cursor()
    return conn, cur


def load_sql_queries(config_file):
    """
    Load SQL queries from an `.ini` file.
    :param config_file: Path to the SQL queries file.
    :return: ConfigParser object with loaded SQL queries.
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    return config
