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
    print("Trying to acquire create_game lock")
    games_lock.acquire()
    print("Create_game lock acquired")
    try:
        num_pairs = int(num_pairs)
        game = Game(num_pairs)
        game_id = id(game)

        games[game_id] = game

        return jsonify(game_id), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create game: {str(e)}"}), 500
    finally:
        print("Trying to release create_game lock")
        games_lock.release()
        print("Create_game lock released")


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
    print("Trying to acquire flip lock")
    games_lock.acquire()
    print("Flip lock acquired")
    try:
        game_id = int(game_id)
        card_index = int(card_index)

        game = games[game_id]
        secret_index = game.flip(card_index)

        return jsonify(secret_index), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id or the card id is invalid"}), 400
    finally:
        print("Trying to release flip lock")
        games_lock.release()
        print("Flip lock released")


# route("/get_time/<game_id>")
def get_time(game_id: int | str):
    print("Trying to acquire time lock")
    games_lock.acquire()
    print("Time lock acquired")
    try:
        game = games[int(game_id)]
        return jsonify(game.get_time()), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400
    finally:
        print("Trying to release time lock")
        games_lock.release()
        print("Time lock released")


# route("/get_flip_count/<game_id>")
def get_flip_count(game_id: int | str):
    print("Trying to acquire flip_count lock")
    games_lock.acquire()
    print("Flip_count lock acquired")
    try:
        game = games[int(game_id)]
        return jsonify(game.get_flip_count()), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400
    finally:
        print("Trying to release flip_count lock")
        games_lock.release()
        print("Flip_count lock released")


# route("/reset_game/<game_id>")
def reset_game(game_id: int | str):
    print("Trying to acquire reset lock")
    games_lock.acquire()
    print("Reset lock acquired")
    try:
        game_id = int(game_id)
        num_pairs = games[game_id].get_num_pairs()
        del games[game_id]

        game = Game(num_pairs)
        game_id = id(game)

        games[game_id] = game

        return jsonify(game_id), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400
    finally:
        print("Trying to release reset lock")
        games_lock.release()
        print("Reset lock released")


# route("/detect_game_finish/<game_id>")
def detect_game_finish(game_id: int | str):
    print("Trying to acquire detect_game_finish lock")
    games_lock.acquire()
    print("Detect_game_finish lock acquired")
    try:
        game_id = int(game_id)
        game = games[game_id]
        return jsonify(game.detect_finished()), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400
    finally:
        print("Trying to release detect_game_finish lock")
        games_lock.release()
        print("Detect_game_finish lock released")


# route(/delete_game/<game_id>)
def delete_game(game_id: int | str):
    print("Trying to acquire delete_game lock")
    games_lock.acquire()
    print("Delete_game lock acquired")
    try:
        game_id = int(game_id)
        del games[game_id]
        return jsonify(True), 201
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400
    finally:
        print("Trying to release delete_game lock")
        games_lock.release()
        print("Delete_game lock released")


# route(/submit_game/<game_id>/<player_name>)
def submit_game(game_id: int | str, player_name: str):
    print("Trying to acquire submit lock")
    games_lock.acquire()
    print("Submit lock acquired")
    try:
        game_id = int(game_id)
        game = games[game_id]
        return game.submit_score(player_name)
    except KeyError:
        return jsonify({"error": "The game doesn't exist"}), 400
    except ValueError:
        return jsonify({"error": "The game id is invalid"}), 400
    finally:
        print("Trying to release submit lock")
        games_lock.release()
        print("Submit lock release")
