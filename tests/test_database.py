from unittest.mock import patch
from datetime import datetime, timezone
from app_logic.models import PlayerScore, db


def test_submit_score(client):
    """Test the /submit_score route with valid data."""
    payload = {
        "player_name": "Test Player",
        "completion_time": 120.5,
        "moves": 30,
    }
    response = client.post("/submit_score", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["player_name"] == "Test Player"
    assert data["completion_time"] == 120.5
    assert data["moves"] == 30


def test_internal_submit_score(client, app):
    """Test the internal_submit_score function."""
    # Test case 1: Valid input data
    with app.app_context():
        from app_logic.database_routes import internal_submit_score
        from app_logic.models import PlayerScore

        player_name = "Test Player"
        completion_time = 120.5
        moves = 30

        # Call the function directly
        response = internal_submit_score(player_name, completion_time, moves)
        assert response[1] == 201  # Ensure it returns a 201 status code
        data = response[0].json
        assert data["player_name"] == player_name
        assert data["completion_time"] == completion_time
        assert data["moves"] == moves

        # Verify the data is persisted in the database
        persisted_score = PlayerScore.query.filter_by(
            player_name=player_name
        ).first()
        assert persisted_score is not None
        assert persisted_score.player_name == player_name
        assert persisted_score.completion_time == completion_time
        assert persisted_score.moves == moves

    # Test case 2: Invalid input data (missing player_name)
    with app.app_context():
        from app_logic.database_routes import internal_submit_score

        response = internal_submit_score(None, completion_time, moves)
        assert response[1] == 500  # Ensure it returns a 500 status code
        data = response[0].json
        assert "error" in data

    # Test case 3: Handle database error
    with app.app_context():
        from app_logic.database_routes import internal_submit_score
        from unittest.mock import patch

        with patch("app_logic.models.db.session.add") as mock_add:
            mock_add.side_effect = Exception("Database error")

            response = internal_submit_score(
                player_name, completion_time, moves
            )
            assert response[1] == 500  # Ensure it returns a 500 status code
            data = response[0].json
            assert "error" in data
            assert "Database error" in data["error"]


def test_submit_score_invalid_data(client):
    """Test /submit_score route with invalid data."""
    invalid_payload = {"player_name": "", "completion_time": -5, "moves": -1}
    response = client.post("/submit_score", json=invalid_payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_submit_score_persistence(client, app):
    """Test if submitted scores persist in the database."""
    payload = {
        "player_name": "Persistent Player",
        "completion_time": 100.0,
        "moves": 25,
    }
    response = client.post("/submit_score", json=payload)
    assert response.status_code == 201

    # Query the database directly to validate persistence
    with app.app_context():
        from app_logic.models import PlayerScore

        scores = PlayerScore.query.filter_by(
            player_name="Persistent Player"
        ).all()
        assert len(scores) == 1
        assert scores[0].completion_time == 100.0
        assert scores[0].moves == 25


def test_fetch_leaderboard(client):
    """Test the /fetch_leaderboard route with preloaded data."""
    response = client.get("/fetch_leaderboard")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) <= 10  # Ensure the leaderboard has at most 10 entries


def test_leaderboard_order_and_limit(client, app):
    """Ensure leaderboard is ordered by completion_time and limited nums."""
    # Add multiple entries
    with app.app_context():
        from app_logic.models import PlayerScore, db

        db.session.bulk_save_objects(
            [
                PlayerScore(
                    player_name=f"Player {i}",
                    completion_time=i * 10,
                    moves=20,
                    created_at=datetime.now(timezone.utc),
                )
                for i in range(15)
            ]
        )
        db.session.commit()

    response = client.get("/fetch_leaderboard")
    assert response.status_code == 200
    data = response.get_json()

    assert len(data) == 10  # Limit to top 10 entries
    times = [entry["completion_time"] for entry in data]
    assert times == sorted(times)  # Ensure correct order


def test_empty_leaderboard(client, app):
    """Test the /fetch_leaderboard route with no data."""
    # Ensure database is empty
    with app.app_context():
        from app_logic.models import PlayerScore, db

        db.session.query(PlayerScore).delete()
        db.session.commit()

    response = client.get("/fetch_leaderboard")
    assert response.status_code == 200
    data = response.get_json()
    assert data == []  # Empty leaderboard


def test_get_random_images(client):
    """Test /get_random_images API with real API."""
    response = client.get("/get_random_images?count=5")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 5  # Ensure 5 images are returned
    assert all("url" in image for image in data)  # Ensure each image has a URL

    # Check that URLs are unique
    urls = [image["url"] for image in data]
    assert len(set(urls)) == len(urls), "Image URLs are not unique"


def test_check_player(client, app):
    """Test the /check_player API endpoint."""

    # Add a test player to the database
    with app.app_context():
        test_player = PlayerScore(
            player_name="TestPlayer",
            completion_time=120.5,
            moves=30,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(test_player)
        db.session.commit()

    # Test case 1: Player exists
    response = client.get("/check_player?player_name=TestPlayer")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "True"

    # Test case 2: Player does not exist
    response = client.get("/check_player?player_name=NonExistentPlayer")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "False"

    # Test case 3: Missing player_name parameter
    response = client.get("/check_player")
    assert response.status_code == 400
    assert response.get_data(as_text=True) == "False"

    # Test case 4: Handle database error (simulate failure)
    with patch("app_logic.models.PlayerScore.query") as mock_query:
        mock_query.filter_by.side_effect = Exception(
            "Database connection failed"
        )

        response = client.get("/check_player?player_name=TestPlayer")
        assert response.status_code == 500
        assert response.get_data(as_text=True) == "False"
