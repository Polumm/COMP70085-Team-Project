import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from adbc_driver_postgresql.dbapi import connect
import random
import json  # For converting Python objects to JSON
from datetime import datetime, timezone
import configparser

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


def create_app(generate_game=False):
    """
    Flask application factory pattern for creating app instances.
    :param generate_game: Whether to generate new card layouts.
    :return: Configured Flask app instance.
    """
    app = Flask(__name__, template_folder=os.path.abspath("templates"))

    # Load sensitive configurations from environment variables
    target_db_url = os.getenv("TARGET_DB_URL")  # Database URL for PostgreSQL
    flask_db_url = os.getenv(
        "FLASK_DB_URL"
    )  # SQLAlchemy database URL for Flask

    if not target_db_url or not flask_db_url:
        raise RuntimeError(
            "Missing required environment variables: "
            "TARGET_DB_URL and FLASK_DB_URL"
        )

    # Load SQL queries from the configuration file
    sql_queries = load_sql_queries("app_logic/sql_queries.ini")

    # Initialize target database connections
    target_conn, target_cur = init_db_connection(target_db_url)

    # Create tables in the target database
    target_cur.execute(sql_queries["table_creation"]["create_card_layouts"])
    target_cur.execute(sql_queries["table_creation"]["create_player_scores"])

    # Optionally generate and save card layouts
    if generate_game:
        for _ in range(5):  # Generate 5 example layouts
            layout = generate_card_layout()
            layout_json = json.dumps(layout)  # Convert layout to JSON format
            target_cur.execute(
                sql_queries["insert_queries"]["insert_card_layout"],
                (layout_json, datetime.now(timezone.utc)),
            )

        # Commit changes to the database
        target_conn.commit()

    # Close database connections
    target_cur.close()
    target_conn.close()

    # Flask SQLAlchemy and Migrate configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = flask_db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register API routes
    from app_logic.routes import api

    app.register_blueprint(api, url_prefix="/")

    return app
