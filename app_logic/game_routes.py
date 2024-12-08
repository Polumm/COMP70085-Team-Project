from flask import jsonify


from game_logic.game_state import Game, games, games_lock
from app_logic.database import db


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

        games_lock.acquire()
        games[game_id] = game
        games_lock.release()

        return jsonify(game_id), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create game: {str(e)}"}), 500


# route("/create_default_game", methods=["POST"])
def create_default_game():
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

        games_lock.acquire()
        game = games[game_id]
        secret_index = game.flip(card_index)
        games_lock.release()

        return jsonify(secret_index), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id or the card id is invalid"}), 400


# route("/get_time/<game_id>")
def get_time(game_id: int | str):
    try:
        games_lock.acquire()
        game = games[int(game_id)]
        games_lock.release()
        return jsonify(game.get_time()), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400


# route("/get_flip_count/<game_id>")
def get_flip_count(game_id: int | str):
    try:
        games_lock.acquire()
        game = games[int(game_id)]
        games_lock.release()
        return jsonify(game.get_flip_count()), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400


# route("/reset_game/<game_id>")
def reset_game(game_id: int | str):
    try:
        game_id = int(game_id)
        games_lock.acquire()
        num_pairs = games[game_id].get_num_pairs()
        del games[game_id]
        games_lock.release()
        return create_game(num_pairs)
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400


# route("/detect_game_finish/<game_id>")
def detect_game_finish(game_id: int | str):
    try:
        game_id = int(game_id)
        games_lock.acquire()
        game = games[game_id]
        games_lock.release()
        return jsonify(game.detect_finished()), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400


# route(/delete_game/<game_id>)
def delete_game(game_id: int | str):
    try:
        game_id = int(game_id)
        games_lock.acquire()
        del games[game_id]
        games_lock.release()
        return jsonify(True), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400


# route(/submit_game/<game_id>/<player_name>)
def submit_game(game_id: int | str, player_name: str):
    try:
        game_id = int(game_id)
        games_lock.acquire()
        game = games[game_id]
        games_lock.release()
        return game.submit_score(player_name)
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400
