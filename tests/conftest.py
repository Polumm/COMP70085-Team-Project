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
            # Add a secret key for sessions
            "SECRET_KEY": "some_random_secret_key_for_testing",
        }
    )
    register_apis(app, __name__)
    yield app


@pytest.fixture(scope="function", autouse=True)
def clean_db(app):
    """
    Before each test function, drop all tables and create them again
    to ensure a clean database state.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield


@pytest.fixture(scope="function", autouse=True)
def rollback_session(app):
    """
    Start a transaction for each test and rollback after the test ends.
    """
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        db.session.bind = connection
        yield
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="module")
def client(app):
    """Provide a test client for the Flask application."""
    return app.test_client()
