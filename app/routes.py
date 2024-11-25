from flask import Blueprint, jsonify, request
from app.models import db, CardLayout, PlayerScore
import random

api = Blueprint('api', __name__)

@api.route('/create_game', methods=['POST'])
def create_game():
    """
    Create a new game card layout
    - Generates a random shuffled card layout
    - Saves the layout to the database
    """
    # Generate a shuffled card layout (each card appears twice)
    cards = list(range(1, 9)) * 2
    random.shuffle(cards)

    # Save the layout in the database
    new_layout = CardLayout(layout=cards)
    db.session.add(new_layout)
    db.session.commit()

    return jsonify(new_layout.to_dict()), 201

@api.route('/submit_score', methods=['POST'])
def submit_score():
    """
    Submit a player's score
    - Accepts player name, completion time, and number of moves as JSON
    - Saves the score to the database
    """
    data = request.get_json()
    player_name = data.get('player_name')
    completion_time = data.get('completion_time')
    moves = data.get('moves')

    if not player_name or completion_time is None or moves is None:
        return jsonify({'error': 'Invalid data'}), 400

    # Create a new player score entry
    new_score = PlayerScore(
        player_name=player_name,
        completion_time=completion_time,
        moves=moves
    )
    db.session.add(new_score)
    db.session.commit()

    return jsonify(new_score.to_dict()), 201

@api.route('/leaderboard', methods=['GET'])
def leaderboard():
    """
    Retrieve the leaderboard
    - Returns the top 10 players sorted by completion time
    """
    scores = PlayerScore.query.order_by(PlayerScore.completion_time.asc()).limit(10).all()
    return jsonify([score.to_dict() for score in scores])
