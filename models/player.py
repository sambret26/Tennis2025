from datetime import datetime
from sqlalchemy.orm import relationship

from database import db

class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fft_id = db.Column(db.String, unique=True, index=True)
    inscription_id = db.Column(db.String, unique=True, index=True)
    last_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    ranking_id = db.Column(db.Integer) #, db.ForeignKey("rankings.id"))
    club = db.Column(db.String)
    state = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    # ranking = relationship("Ranking", back_populates="players")
    # matches_as_player1 = relationship("Match", foreign_keys="[Match.player1_id]", back_populates="player1")
    # matches_as_player2 = relationship("Match", foreign_keys="[Match.player2_id]", back_populates="player2")
    # matches_won = relationship("Match", foreign_keys="[Match.winner_id]", back_populates="winner")
    # categories = relationship("Category", secondary="player_categories", back_populates="players")
    # availabilities = relationship("Availability", back_populates="player")
    # payments = relationship("Payment", back_populates="player")
    # balance = relationship("PlayerBalance", back_populates="player", uselist=False)

    def __init__(self, fft_id, inscription_id, last_name, first_name, 
            ranking_id, club, state, is_active):
        self.fft_id = fft_id
        self.inscription_id = inscription_id
        self.last_name = last_name
        self.first_name = first_name
        self.ranking_id = ranking_id
        self.club = club
        self.state = state
        self.is_active = is_active

    def to_dict(self):
        return {
            "id": self.id,
            "fft_id": self.fft_id,
            "inscription_id": self.inscription_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "ranking_id": self.ranking_id,
            "club": self.club,
            "state": self.state,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }