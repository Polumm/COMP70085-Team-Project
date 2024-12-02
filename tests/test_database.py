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
