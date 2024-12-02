from flask import render_template


# @api.route("/")
def index():
    return render_template("index.html")


# @api.route("/game")
def game():
    return render_template("game.html")
