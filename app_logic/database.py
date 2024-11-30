import configparser
from adbc_driver_postgresql.dbapi import connect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import random


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


def generate_card_layout(num_pairs=8):
    """
    Generate a shuffled card layout for the game.
    :param num_pairs: Number of unique card pairs to generate.
    :return: A shuffled list of card pairs.
    """
    cards = list(range(1, num_pairs + 1)) * 2  # Create pairs
    random.shuffle(cards)  # Shuffle the cards
    return cards


def load_sql_queries(config_file):
    """
    Load SQL queries from an `.ini` file.
    :param config_file: Path to the SQL queries file.
    :return: ConfigParser object with loaded SQL queries.
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    return config
