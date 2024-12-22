from datetime import datetime
from database import db

class PlayerAvailability(db.Model):
    __tablename__ = "player_availabilities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerId = db.Column(db.Integer, db.ForeignKey("players.id"), index=True)
    day = db.Column(db.String, nullable=False)
    timeSlot = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, playerId, day, timeSlot, available):
        self.playerId = playerId
        self.day = day
        self.timeSlot = timeSlot
        self.available = available

    def toDict(self):
        return {
            "id": self.id,
            "playerId": self.playerId,
            "day": self.day,
            "timeSlot": self.timeSlot,
            "available": self.available
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            playerId=data['playerId'],
            day=data['day'],        
            timeSlot=data['timeSlot'],        
            available=data['available']
        )