from flask import jsonify

from datetime import datetime, timezone

from game_logic.game_state import Game, games
from app_logic.database import db
from app_logic.models import CardLayout


# route("/create_game/<num_pairs>", methods=["POST"])
def create_game(num_pairs: int | str):
    """
    Create a new game card layout
    - Generates a random shuffled card layout (each card appears twice).
    - Saves the layout into the database.

    Returns:
        The created card layout in JSON format.
    """
    try:
        num_pairs = int(num_pairs)
        game = Game(num_pairs)
        game_id = id(game)

        # Save the layout in the database
        layout = CardLayout(layout=None, created_at=datetime.now(timezone.utc))
        db.session.add(layout)
        db.session.commit()

        return jsonify(game_id), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create game: {str(e)}"}), 500


# route("/create_default_game", methods=["POST"])
def create_default_game(num_pairs: int | str):
    """
    Create a new game card layout
    - Generates a random shuffled card layout (each card appears twice).
    - Saves the layout into the database.

    Returns:
        The created card layout in JSON format.
    """
    return create_game(10)


# route("/flip/<game_id>/<card_index>", methods=["POST"])
def flip(game_id: int | str, card_index: int | str):
    try:
        game_id = int(game_id)
        card_index = int(card_index)
        secret_index = games[game_id].flip(card_index)
        return jsonify(secret_index), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id or the card id is invalid"}), 400


# route("/get_time/<game_id>")
def get_time(game_id: int | str):
    try:
        game = games[int(game_id)]
        return jsonify(game.get_time()), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400


# route("/get_flip_count/<game_id>")
def get_flip_count(game_id: int | str):
    try:
        game = games[int(game_id)]
        return jsonify(game.get_flip_count()), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400


# route("/reset_game/<game_id>")
def reset_game(game_id: int | str):
    try:
        game_id = int(game_id)
        num_pairs = games[game_id].get_num_pairs()
        del games[game_id]
        return create_game(num_pairs)
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400


# route("/detect_game_finish/<game_id>")
def detect_game_finish(game_id: int | str):
    try:
        game_id = int(game_id)
        game = games[game_id]
        return jsonify(game.detect_finished()), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400


# route(/delete_game/<game_id>)
def delete_game(game_id: int | str):
    try:
        game_id = int(game_id)
        del games[game_id]
        return jsonify(True), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400
