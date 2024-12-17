from datetime import datetime
from database import db

class Availability(db.Model):
    __tablename__ = "availabilities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerId = db.Column(db.Integer, db.ForeignKey("players.id"), index=True)
    day = db.Column(db.String, nullable=False)
    hour = db.Column(db.String, nullable=False)
    available = db.Column(db.String, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, playerId, day, hour, available):
        self.playerId = playerId
        self.day = day
        self.hour = hour
        self.available = available

    def toDict(self):
        return {
            "id": self.id,
            "playerId": self.playerId,
            "day": self.day,
            "hour": self.hour,
            "available": self.available
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            playerId=data['playerId'],
            day=data['day'],        
            hour=data['hour'],        
            available=data['available']
        )