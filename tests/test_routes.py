from app_logic.database import db
from app_logic.models import PlayerScore


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
    assert (
        response.status_code == 201
    ), f"The status code is {response.status_code}"
    data = response.get_json()
    assert "layout" in data
