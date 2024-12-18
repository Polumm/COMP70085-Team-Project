from datetime import datetime, timezone

from app_logic.database import db


class PlayerScore(db.Model):
    """Model for storing player scores and performance metrics."""

    __tablename__ = "player_scores"
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    player_name = db.Column(
        db.String(50), nullable=False, index=True
    )  # Player's name
    completion_time = db.Column(
        db.Float, nullable=False, index=True
    )  # Time taken to complete the game
    moves = db.Column(
        db.Integer, nullable=False
    )  # Number of moves taken to complete the game
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )  # Timestamp when the score is recorded

    def to_dict(self):
        """Convert model instance to dictionary for serialization."""
        return {
            "id": self.id,
            "player_name": self.player_name,
            "completion_time": self.completion_time,
            "moves": self.moves,
            "created_at": self.created_at.isoformat(),
        }

    @staticmethod
    def validate_score(player_name, completion_time, moves):
        """
        Validate player score data before saving.
        :param player_name: Name of the player.
        :param completion_time: Time taken to complete the game.
        :param moves: Number of moves taken.
        :return: Validated data tuple (player_name, completion_time, moves).
        """
        if not player_name or not isinstance(player_name, str):
            raise ValueError("Player name must be a non-empty string.")
        if (
            not isinstance(completion_time, (int, float))
            or completion_time <= 0
        ):
            raise ValueError("Completion time must be a positive number.")
        if not isinstance(moves, int) or moves <= 0:
            raise ValueError("Moves must be a positive integer.")
        return player_name, completion_time, moves
