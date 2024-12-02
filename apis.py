from flask import Blueprint

from app_logic.database_routes import (
    leaderboard,
    submit_score,
)
from app_logic.game_routes import (
    create_game,
    flip,
    get_time,
    get_flip_count,
    reset_game,
    delete_game,
    detect_game_finish,
)
from app_logic.page_routes import game, index
from app_logic.fetch_image_routes import get_random_images


frontend_apis = {
    "/": (index, ["GET"]),
    "/game": (game, ["GET"]),
}

database_apis = {
    "/leaderboard": (leaderboard, ["GET"]),
    "/submit_score": (submit_score, ["POST"]),
}

fetch_image_apis = {
    "/get_random_images": (get_random_images, ["GET"]),
}

game_apis = {
    "/create_game/<num_pairs>": (create_game, ["POST"]),
    "/flip/<game_id>/<card_index>": (flip, ["POST"]),
    "/get_time/<num_pairs>": (get_time, ["GET"]),
    "/get_flip_count/<num_pairs>": (get_flip_count, ["GET"]),
    "/reset_game/<num_pairs>": (reset_game, ["POST"]),
    "/delete_game/<num_pairs>": (delete_game, ["POST"]),
    "/detect_game_finish/<num_pairs>": (detect_game_finish, ["GET"]),
}


def register_apis(app, name: str):
    apis = Blueprint("apis", name)

    for api_set in (frontend_apis, database_apis, fetch_image_apis, game_apis):
        for route, (func, method) in api_set.items():
            apis.route(route, methods=method)(func)

    app.register_blueprint(apis)
