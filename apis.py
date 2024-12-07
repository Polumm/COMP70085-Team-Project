from flask import Blueprint

from app_logic.database_routes import (
    fetch_leaderboard,
    submit_score,
    check_player,
)
from app_logic.game_routes import (
    create_game,
    create_default_game,
    flip,
    get_time,
    get_flip_count,
    reset_game,
    delete_game,
    detect_game_finish,
    submit_game,
)
from app_logic.page_routes import game, index, leaderboard
from app_logic.fetch_image_routes import get_random_images


frontend_apis = {
    "/": (index, ["GET"]),
    "/game": (game, ["GET"]),
    "/leaderboard": (leaderboard, ["GET"]),
}

database_apis = {
    "/fetch_leaderboard": (fetch_leaderboard, ["GET"]),
    "/submit_score": (submit_score, ["POST"]),
    "/check_player": (check_player, ["GET"]),
}

fetch_image_apis = {
    "/get_random_images": (get_random_images, ["GET"]),
}

game_apis = {
    "/create_game/<num_pairs>": (create_game, ["POST"]),
    "/create_default_game": (create_default_game, ["POST"]),
    "/flip/<game_id>/<card_index>": (flip, ["POST"]),
    "/get_time/<game_id>": (get_time, ["GET"]),
    "/get_flip_count/<game_id>": (get_flip_count, ["GET"]),
    "/reset_game/<game_id>": (reset_game, ["POST"]),
    "/delete_game/<game_id>": (delete_game, ["POST"]),
    "/detect_game_finish/<game_id>": (detect_game_finish, ["GET"]),
    "/submit_game/<game_id>": (submit_game, ["GET"]),
}


def register_apis(app, name: str):
    apis = Blueprint("apis", name)

    for api_set in (
        frontend_apis,
        database_apis,
        fetch_image_apis,
        game_apis,
    ):
        for route, (func, method) in api_set.items():
            apis.route(route, methods=method)(func)

    app.register_blueprint(apis)
