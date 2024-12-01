from flask import Blueprint

from app_logic.routes import (
    game,
    leaderboard,
    create_game,
    submit_score,
    get_card_layouts,
    get_random_images,
    index,
    flip,
)


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
        api.route(route, method=method)(func)

    for route, (func, method) in backend_apis.items():
        api.route(route, method=method)(func)

    app.register_blueprint(api)
