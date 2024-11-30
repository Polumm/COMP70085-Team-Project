# from flask import render_template

import os

from flask import render_template

from app_logic.init_app import create_app
from app_logic.routes import (
    game,
    leaderboard,
    create_game,
    submit_score,
    get_card_layouts,
    get_random_images,
    index,
)

app = create_app(__name__, os.path.abspath("templates"))

# frontend apis
app.route("/")(index)
app.route("/game")(game)

# backend apis
app.route("/leaderboard", methods=["GET"])(leaderboard)
app.route("/create_game", methods=["POST"])(create_game)
app.route("/submit_score", methods=["POST"])(submit_score)
app.route("/get_card_layouts", methods=["GET"])(get_card_layouts)
app.route("/get_random_images", methods=["GET"])(get_random_images)


@app.route("/test")
def test():
    return render_template(
        """<div class="button-container">
        <a href="game" class="button">{{1+1}}</a>
        <a href="leaderboard" class="button">View Leaderboard</a>
      </div>"""
    )
