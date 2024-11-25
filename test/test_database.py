import pytest
from app import create_app, db
from app.models import CardLayout, PlayerScore


@pytest.fixture
def app():
    """Set up Flask app for testing."""
    app = create_app(generate_game=False)
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            # Use in-memory SQLite for tests
        }
    )

    with app.app_context():
        db.create_all()  # Create tables for models
        yield app  # Provide app for testing
        db.session.remove()
        db.drop_all()  # Clean up after tests


@pytest.fixture
def client(app):
    """Provide test client for API."""
    return app.test_client()


def test_card_layout_model(app):
    """Test CardLayout model CRUD operations."""
    with app.app_context():
        # Create a card layout
        layout = CardLayout(
            layout=[1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8]
        )
        db.session.add(layout)
        db.session.commit()

        # Check if the layout is saved
        retrieved_layout = CardLayout.query.first()
        assert retrieved_layout is not None
        assert retrieved_layout.layout == layout.layout


def test_player_score_model(app):
    """Test PlayerScore model CRUD operations."""
    with app.app_context():
        # Create a player score
        score = PlayerScore(
            player_name="Test Player", completion_time=45.5, moves=20
        )
        db.session.add(score)
        db.session.commit()

        # Check if the score is saved
        retrieved_score = PlayerScore.query.first()
        assert retrieved_score is not None
        assert retrieved_score.player_name == "Test Player"
        assert retrieved_score.completion_time == 45.5
        assert retrieved_score.moves == 20
