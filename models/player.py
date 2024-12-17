from datetime import datetime
from sqlalchemy.orm import relationship
from models.Availability import Availability

from database import db

class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.String, unique=True, index=True)
    inscriptionId = db.Column(db.String, unique=True, index=True)
    lastName = db.Column(db.String, nullable=False)
    firstName = db.Column(db.String, nullable=False)
    rankingId = db.Column(db.Integer) #, db.ForeignKey("rankings.id"))
    club = db.Column(db.String)
    isActive = db.Column(db.Boolean, default=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    # ranking = relationship("Ranking", back_populates="players")
    # matches_as_player1 = relationship("Match", foreign_keys="[Match.player1_id]", back_populates="player1")
    # matches_as_player2 = relationship("Match", foreign_keys="[Match.player2_id]", back_populates="player2")
    # matches_won = relationship("Match", foreign_keys="[Match.winner_id]", back_populates="winner")
    # categories = relationship("Category", secondary="player_categories", back_populates="players")
    # payments = relationship("Payment", back_populates="player")
    # balance = relationship("PlayerBalance", back_populates="player", uselist=False)

    def __init__(self, fftId, inscriptionId, lastName, firstName, 
            rankingId, club, isActive):
        self.fftId = fftId
        self.inscriptionId = inscriptionId
        self.lastName = lastName
        self.firstName = firstName
        self.rankingId = rankingId
        self.club = club
        self.isActive = isActive

    def toDict(self):
        return {
            "id": self.id,
            "fftId": self.fftId,
            "inscriptionId": self.inscriptionId,
            "lastName": self.lastName,
            "firstName": self.firstName,
            "rankingId": self.rankingId,
            "club": self.club,
            "isActive": self.isActive
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            inscriptionId=data['inscriptionId'],        
            lastName=data['lastName'],        
            firstName=data['firstName'],        
            rankingId=data['rankingId'],        
            club=data['club'],        
            isActive=data['isActive']
        )