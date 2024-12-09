from app_logic.database import db
from app_logic.models import PlayerScore


def test_player_score_model(app):
    """Test PlayerScore model CRUD operations."""
    with app.app_context():
        # Create a player score
        score = PlayerScore(
            player_name="TestPlayer", completion_time=120.5, moves=30
        )
        db.session.add(score)
        db.session.commit()

        # Query the score
        queried_score = PlayerScore.query.first()
        assert (
            queried_score.player_name == "TestPlayer"
        ), f"Expected 'TestPlayer', got '{queried_score.player_name}'"
