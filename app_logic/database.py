import configparser
from adbc_driver_postgresql.dbapi import connect
from flask import jsonify
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


def internal_submit_score(player_name, completion_time, moves):
    try:
        # Create a new player score entry
        score = PlayerScore(
            player_name=player_name,
            completion_time=float(completion_time),
            moves=moves,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(score)
        db.session.commit()

        return jsonify(score.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to submit score: {str(e)}"}), 500
