from datetime import datetime, timezone
from flask import jsonify, request


from app_logic.models import PlayerScore
from app_logic.database import db


# ==============================
# API ENDPOINTS
# ==============================


# @api.route("/fetch_leaderboard", methods=["GET"])
def fetch_leaderboard():
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


# @api.route("/submit_score", methods=["POST"])
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

    return internal_submit_score(player_name, completion_time, moves)


def internal_submit_score(player_name, completion_time, moves):
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


def check_player():
    """
    Check if a player is already registered.
    - Accepts a player_name as a query parameter.
    - Queries the database to check if the player exists.

    Query Parameters:
        player_name (str): The name of the player to check.

    Returns:
        True if the player exists, False otherwise.
    """
    player_name = request.args.get("player_name", default=None, type=str)

    if not player_name:
        return (
            "False",
            400,
        )  # Return False with HTTP 400 status for missing parameter

    try:
        # Query the database to check if the player exists
        exists = (
            PlayerScore.query.filter_by(player_name=player_name).first()
            is not None
        )
        return str(exists), 200
    except Exception as e:
        # Log the exception if needed
        print(f"Error checking player: {e}")
        return (
            "False",
            500,
        )  # Return False with HTTP 500 status for server error


def check_player_existence(player_name):
    """
    Internal helper function to check if a player already exists.
    replicates the logic of the check_player endpoint, but works internally.
    """
    if not player_name:
        # If no name provided, treat as not found.
        return False

    try:
        # Check if the player exists in the database
        exists = (
            PlayerScore.query.filter_by(player_name=player_name).first()
            is not None
        )
        return exists
    except Exception as e:
        # In case of any database error, log the error and assume not found.
        # You can customize error handling as needed.
        print(f"Error checking player internally: {e}")
        return False
