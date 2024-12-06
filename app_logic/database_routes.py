from flask import jsonify, request

from datetime import datetime, timezone

from app_logic.models import db, PlayerScore


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
