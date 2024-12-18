from datetime import datetime
from database import db

class Reduction(db.Model):
    __tablename__ = 'reductions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerId = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    reason = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, playerId, reason, amount):
        self.playerId = playerId
        self.reason = reason
        self.amount = amount

    def toDict(self):
        return {
            'id': self.id,
            'playerId': self.playerId,
            'reason': self.reason,
            'amount': self.amount
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            playerId=data['playerId'],
            reason=data['reason'],
            amount=data['amount']
        )