from flask import Blueprint

from app_logic.database_routes import (
    leaderboard,
    submit_score,
    get_card_layouts,
)
from app_logic.game_routes import create_game, flip
from app_logic.page_routes import game, index
from app_logic.fetch_image_routes import get_random_images


frontend_apis = {
    "/": (index, ["GET"]),
    "/game": (game, ["GET"]),
}

backend_apis = {
    "/leaderboard": (leaderboard, ["GET"]),
    "/create_game/<num_pairs>": (create_game, ["POST"]),
    "/submit_score": (submit_score, ["POST"]),
    "/get_card_layouts": (get_card_layouts, ["GET"]),
    "/get_random_images": (get_random_images, ["GET"]),
    "/flip/<game_id>/<card_index>": (flip, ["POST"]),
}


def register_apis(app, name: str):
    api = Blueprint("apis", name)

    for route, (func, method) in frontend_apis.items():
        api.route(route, methods=method)(func)

    for route, (func, method) in backend_apis.items():
        api.route(route, methods=method)(func)

    app.register_blueprint(api)
