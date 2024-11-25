import configparser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from adbc_driver_postgresql.dbapi import connect
import random
import json  # For converting Python objects to JSON
from datetime import datetime

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()


def load_config(config_file):
    """
    Load configuration from a specified `.ini` file.
    :param config_file: Path to the configuration file.
    :return: ConfigParser object with loaded configurations.
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


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


def create_app():
    """
    Flask application factory pattern for creating app instances.
    :return: Configured Flask app instance.
    """
    app = Flask(__name__)

    # Load configurations
    secret_config = load_config(
        "app/secret.ini"
    )  # Secrets for target database
    sql_config = load_config(
        "app/sql_queries.ini"
    )  # SQL queries for target databases

    # PostgreSQL connection URLs
    target_db_url = secret_config["database"]["db_url"]

    # Initialize target database connections
    target_conn, target_cur = init_db_connection(target_db_url)

    # Create target tables
    target_cur.execute(sql_config["table_creation"]["create_card_layouts"])
    target_cur.execute(sql_config["table_creation"]["create_player_scores"])

    # Generate and save card layouts
    for _ in range(5):  # Generate 5 example layouts
        layout = generate_card_layout()
        layout_json = json.dumps(layout)  # Convert layout to JSON format
        target_cur.execute(
            """
            INSERT INTO card_layouts (layout, created_at)
            VALUES ($1::jsonb, $2)
            """,
            (layout_json, datetime.utcnow()),
        )

    # Commit changes to the database
    target_conn.commit()

    # Close database connections
    target_cur.close()
    target_conn.close()

    # Flask SQLAlchemy and Migrate configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = secret_config["flask"]["db_url"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    return app
