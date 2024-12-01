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


# Create a Blueprint for API routes
def register_apis(app, name: str):
    api = Blueprint("api", name)

    # frontend apis
    api.route("/")(index)
    api.route("/game")(game)

    # backend apis
    api.route("/leaderboard", methods=["GET"])(leaderboard)
    api.route("/create_game/<num_pairs>", methods=["POST"])(create_game)
    api.route("/submit_score", methods=["POST"])(submit_score)
    api.route("/get_card_layouts", methods=["GET"])(get_card_layouts)
    api.route("/get_random_images", methods=["GET"])(get_random_images)
    api.route("/flip/<game_id>/<card_index>", methods=["POST"])(flip)

    app.register_blueprint(api)
