import pytest
from app import create_app, db
from app.models import CardLayout, PlayerScore
import os


@pytest.fixture(scope="module")
def app():
    """Create a Flask application for testing."""
    app = create_app(generate_game=False)  # Disable card layout generation
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


# Test cases
def test_card_layout_contains_pairs(app):
    """Test if the card layout contains pairs of each card."""
    with app.app_context():
        # Create a test card layout
        layout_data = [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8]
        layout = CardLayout(layout=layout_data)
        db.session.add(layout)
        db.session.commit()

        # Query the layout
        queried_layout = CardLayout.query.first()

        # Verify the card layout contains pairs
        card_counts = {}
        for card in queried_layout.layout:
            card_counts[card] = card_counts.get(card, 0) + 1

        assert all(
            count == 2 for count in card_counts.values()
        ), f"Card layout does not contain pairs: {card_counts}"


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
    response = client.post("/create_game")
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
