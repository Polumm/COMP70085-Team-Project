import pytest

import os

from apis import register_apis
from app_logic.init_app import create_app
from app_logic.database import db


@pytest.fixture(scope="module")
def app():
    """Create a Flask application for testing."""
    app = create_app(__name__, isTest=True)
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": os.getenv("TEST_TARGET_DB_URL"),
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )
    register_apis(app, __name__)
    with app.app_context():
        yield app


@pytest.fixture(scope="function", autouse=True)
def rollback_session(app):
    """
    Ensure each test runs in a rolled-back transaction.
    This keeps the database state unchanged after the test.
    """
    with app.app_context():
        connection = db.engine.connect()  # Connect to the database
        transaction = connection.begin()  # Begin a transaction
        db.session.bind = connection  # Bind the session to the transaction
        yield  # Run the test
        transaction.rollback()  # Rollback all changes made during the test
        connection.close()  # Close the database connection


@pytest.fixture(scope="module")
def client(app):
    """Provide a test client for the Flask application."""
    return app.test_client()
