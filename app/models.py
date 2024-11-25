from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class CardLayout(db.Model):
    """Model for storing game card layouts"""
    __tablename__ = 'card_layouts'
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    layout = db.Column(JSONB, nullable=False)  # Card layout stored as JSONB
    created_at = db.Column(db.DateTime, default=datetime, index=True)  # Timestamp when the layout is created

    def to_dict(self):
        """Convert model instance to dictionary for serialization"""
        return {
            'id': self.id,
            'layout': self.layout,
            'created_at': self.created_at.isoformat()
        }

class PlayerScore(db.Model):
    """Model for storing player scores and performance metrics"""
    __tablename__ = 'player_scores'
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier
    player_name = db.Column(db.String(50), nullable=False, index=True)  # Player's name
    completion_time = db.Column(db.Float, nullable=False, index=True)  # Time taken to complete the game
    moves = db.Column(db.Integer, nullable=False)  # Number of moves taken to complete the game
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # Timestamp when the score is recorded

    def to_dict(self):
        """Convert model instance to dictionary for serialization"""
        return {
            'id': self.id,
            'player_name': self.player_name,
            'completion_time': self.completion_time,
            'moves': self.moves,
            'created_at': self.created_at.isoformat()
        }
