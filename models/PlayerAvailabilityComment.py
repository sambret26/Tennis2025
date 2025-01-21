from datetime import datetime
from database import db

class PlayerAvailabilityComment(db.Model):
    __tablename__ = "player_availabilities_comments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerId = db.Column(db.Integer, db.ForeignKey("players.id"), index=True)
    day = db.Column(db.String, nullable=False)
    comments = db.Column(db.String, nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, playerId, day, comments=None):
        self.playerId = playerId
        self.day = day
        self.comments = comments

    def toDict(self):
        return {
            "id": self.id,
            "playerId": self.playerId,
            "day": self.day,
            "comments": self.comments
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            playerId=data['playerId'],
            day=data['day'],
            comments=data.get('comments')  # Utilisation de get() pour gérer le cas où comments est absent
        )
