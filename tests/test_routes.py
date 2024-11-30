import pytest

import os

from app_logic.database import db
from app_logic.models import CardLayout, PlayerScore
from app_logic.init_app import create_app


@pytest.fixture(scope="module")
def app():
    """Create a Flask application for testing."""
    app = create_app(
        __name__, generate_game=False
    )  # Disable card layout generation
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": os.getenv("FLASK_DB_URL"),
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )
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


def test_player_score_model(app):
    """Test PlayerScore model CRUD operations."""
    with app.app_context():
        # Create a player score
        score = PlayerScore(
            player_name="Test Player", completion_time=123.45, moves=30
        )
        db.session.add(score)
        db.session.commit()

        # Query the score
        queried_score = PlayerScore.query.first()
        assert queried_score.player_name == "Test Player"
        assert queried_score.completion_time == 123.45
        assert queried_score.moves == 30


def test_create_game(client):
    """Test the /create_game route."""
    response = client.post("/create_game/10")
    assert response.status_code == 201
    data = response.get_json()
    assert "layout" in data


def test_submit_score(client):
    """Test the /submit_score route."""
    payload = {
        "player_name": "Test Player",
        "completion_time": 120.5,
        "moves": 30,
    }
    response = client.post("/submit_score", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["player_name"] == "Test Player"


def test_leaderboard(client):
    """Test the /leaderboard route."""
    response = client.get("/leaderboard")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_card_layouts_with_pairs(client, app):
    """Test if the card layout contains pairs of numbers in sorted order."""
    with app.app_context():
        # Query the layout
        queried_layout = CardLayout.query.first()

        # Sort the layout
        sorted_layout = sorted(queried_layout.layout)

        # Validate pairs
        pair_differences_sum = 0
        for i in range(0, len(sorted_layout), 2):
            assert (
                sorted_layout[i] == sorted_layout[i + 1]
            ), f"Cards {sorted_layout[i]} and {sorted_layout[i + 1]}"
            " are not a pair"
            pair_differences_sum += sorted_layout[i + 1] - sorted_layout[i]

        # Assert the sum of all pair differences is 0
        assert (
            pair_differences_sum == 0
        ), f"Pair differences do not sum to 0: {pair_differences_sum}"


def test_get_random_images(client):
    """Test /get_random_images API with real Likepoems API."""
    # Fetch 5 random images
    response = client.get("/get_random_images?count=5")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 5  # Ensure 5 images are returned
    assert all("url" in image for image in data)  # Ensure each image has a URL

    # Check that URLs are unique
    urls = [image["url"] for image in data]
    print(urls)
    assert len(set(urls)) == len(urls), "Image URLs are not unique"
