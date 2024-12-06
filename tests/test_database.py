from datetime import datetime, timezone


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
    """Ensure leaderboard is ordered by completion_time and limited to 10 entries."""
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
