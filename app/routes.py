from flask import Blueprint, jsonify, request
from app.models import db, CardLayout, PlayerScore
import random
from datetime import datetime, timezone
import aiohttp
import asyncio

# Create a Blueprint for API routes
api = Blueprint("api", __name__)

# ==============================
# API ENDPOINTS
# ==============================


@api.route("/leaderboard", methods=["GET"])
def leaderboard():
    """
    Retrieve the leaderboard
    - Fetches the top 10 players based on the shortest completion time.
    - Players are ranked in ascending order of their completion time.

    Returns:
        JSON list of player scores (top 10)
    """
    try:
        scores = (
            PlayerScore.query.order_by(PlayerScore.completion_time.asc())
            .limit(10)
            .all()
        )
        return jsonify([score.to_dict() for score in scores]), 200
    except Exception as e:
        return jsonify(
            {"error": f"Failed to fetch leaderboard: {str(e)}"}
        ), 500


@api.route("/create_game/<n>", methods=["POST"])
def create_game(n: int | str):
    """
    Create a new game card layout
    - Generates a random shuffled card layout (each card appears twice).
    - Saves the layout into the database.

    Returns:
        The created card layout in JSON format.
    """
    try:
        n = int(n)
        # Generate a shuffled card layout (each card appears twice)
        cards = list(range(1, 9)) * 2
        random.shuffle(cards)

        # Save the layout in the database
        layout = CardLayout(
            layout=cards, created_at=datetime.now(timezone.utc)
        )
        db.session.add(layout)
        db.session.commit()

        return jsonify(layout.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create game: {str(e)}"}), 500


@api.route("/submit_score", methods=["POST"])
def submit_score():
    """
    Submit a player's score
    - Accepts player data
    - (name, completion time, and number of moves) as JSON input.
    - Validates the input and saves the score in the database.

    Request Body:
        {
            "player_name": "John",
            "completion_time": 45.5,
            "moves": 20
        }

    Returns:
        The saved player score in JSON format.
    """
    data = request.get_json()
    player_name = data.get("player_name")
    completion_time = data.get("completion_time")
    moves = data.get("moves")

    # Validate input data
    if (
        not player_name
        or not isinstance(completion_time, (int, float))
        or not isinstance(moves, int)
    ):
        return jsonify(
            {
                "error": "Invalid data: Ensure player_name is a string,"
                " completion_time is a number, and moves is an integer."
            }
        ), 400

    try:
        # Create a new player score entry
        score = PlayerScore(
            player_name=player_name,
            completion_time=float(completion_time),
            moves=moves,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(score)
        db.session.commit()

        return jsonify(score.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to submit score: {str(e)}"}), 500


@api.route("/get_card_layouts", methods=["GET"])
def get_card_layouts():
    """
    Fetch all card layouts from the database
    - Retrieves all saved card layouts (latest first).

    Returns:
        JSON list of card layouts, or an error message if the query fails.
    """
    try:
        # Fetch all card layouts
        layouts = CardLayout.query.order_by(CardLayout.created_at.desc()).all()

        if not layouts:
            return jsonify({"error": "No card layouts available"}), 404

        # Return the layouts as a list of dictionaries
        return jsonify([layout.to_dict() for layout in layouts]), 200

    except Exception as e:
        return jsonify(
            {"error": f"Failed to fetch card layouts: {str(e)}"}
        ), 500


# ==============================
# FETCH RANDOM IMAGES FROM EXTERNAL API
# ==============================

LIKEPOEMS_IMAGE_API = "https://api.likepoems.com/img/bing/"


async def fetch_image(session):
    """
    Fetch a single image from the Likepoems API.
    - Makes an HTTP GET request to the API to retrieve a random image.

    Returns:
        A dictionary containing the URL of the fetched image.
    """
    async with session.get(LIKEPOEMS_IMAGE_API) as response:
        return {"url": str(response.url)}


async def fetch_unique_images_concurrently(num_images):
    """
    Fetch multiple unique images concurrently from the Likepoems API.
    - Ensures the fetched image URLs are unique.

    Args:
        num_images (int): The number of unique images to fetch.

    Returns:
        A list of dictionaries containing unique image URLs.
    """
    unique_urls = set()
    images = []

    async with aiohttp.ClientSession() as session:
        while len(images) < num_images:
            # Calculate remaining images to fetch
            remaining = num_images - len(images)
            tasks = [fetch_image(session) for _ in range(remaining)]
            results = await asyncio.gather(*tasks)

            for image in results:
                if image["url"] not in unique_urls:
                    unique_urls.add(image["url"])
                    images.append(image)

    return images


@api.route("/get_random_images", methods=["GET"])
def get_random_images():
    """
    Fetch a specified number of unique random images from the Likepoems API.
    - Makes concurrent requests to fetch the specified number of unique images.

    Query Parameters:
        count (int, optional): Number of unique images to fetch.

    Returns:
        JSON list of unique image URLs.
    """
    num_images = request.args.get("count", default=8, type=int)
    if num_images <= 0:
        return jsonify(
            {"error": "The number of images must be greater than 0"}
        ), 400

    try:
        # Use asyncio to fetch unique images concurrently
        images = asyncio.run(fetch_unique_images_concurrently(num_images))
        return jsonify(images), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
