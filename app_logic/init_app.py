from flask import Flask
import os


from app_logic.database import (
    init_db_connection,
    load_sql_queries,
    db,
    migrate,
)


def create_app(
    app_name: str, template_folder=os.path.abspath("templates"), isTest=False
):
    """
    Flask application factory pattern for creating app instances.
    :param app_name: Name of the Flask application.
    :param template_folder: Path to the templates folder.
    :param isTest: Whether to use testing or production database URL.
    :return: Configured Flask app instance.
    """
    app = Flask(app_name, template_folder=template_folder)

    # Choose the appropriate database URL based on isTest
    target_db_url = (
        os.getenv("TEST_TARGET_DB_URL")
        if isTest
        else os.getenv("TARGET_DB_URL")
    )
    flask_db_url = (
        os.getenv("TEST_FLASK_DB_URL") if isTest else os.getenv("FLASK_DB_URL")
    )

    if not target_db_url or not flask_db_url:
        raise RuntimeError(
            "Missing required environment variables: "
            f"{'TEST_TARGET_DB_URL' if isTest else 'TARGET_DB_URL'} and "
            f"{'TEST_FLASK_DB_URL' if isTest else 'FLASK_DB_URL'}"
        )

    # Load SQL queries from the configuration file
    sql_queries = load_sql_queries("app_logic/sql_queries.ini")

    # Initialize target database connections
    target_conn, target_cur = init_db_connection(target_db_url)

    # Create tables in the target database
    target_cur.execute(sql_queries["table_creation"]["create_player_scores"])

    # Close database connections
    target_cur.close()
    target_conn.close()

    # Flask SQLAlchemy and Migrate configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = flask_db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    return app
