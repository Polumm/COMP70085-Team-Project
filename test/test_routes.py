import json
import pytest
from app.models import db, CardLayout, PlayerScore


@pytest.fixture
def game_layout():
    """Fixture for creating a sample game layout."""
    return [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8]


def test_create_game(client, game_layout):
    """Test `/create_game` endpoint."""
    response = client.post("/create_game")
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert "layout" in data
    assert len(data["layout"]) == 16  # 8 pairs


def test_submit_score(client):
    """Test `/submit_score` endpoint."""
    # Submit a score
    payload = {"player_name": "John Doe", "completion_time": 30.5, "moves": 15}
    response = client.post(
        "/submit_score",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 201

    # Verify score is saved
    data = response.get_json()
    assert data["player_name"] == "John Doe"
    assert data["completion_time"] == 30.5
    assert data["moves"] == 15


def test_leaderboard(client):
    """Test `/leaderboard` endpoint."""
    # Add some scores to the database
    scores = [
        {"player_name": "Alice", "completion_time": 20.0, "moves": 12},
        {"player_name": "Bob", "completion_time": 25.5, "moves": 14},
        {"player_name": "Charlie", "completion_time": 18.0, "moves": 10},
    ]
    for score in scores:
        client.post(
            "/submit_score",
            data=json.dumps(score),
            content_type="application/json",
        )

    # Get leaderboard
    response = client.get("/leaderboard")
    assert response.status_code == 200

    # Check leaderboard structure
    data = response.get_json()
    assert len(data) == 3  # Three scores added
    assert data[0]["player_name"] == "Charlie"  # Best time first
