from datetime import datetime
from database import db

class Reduction(db.Model):
    __tablename__ = 'reductions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerId = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    reason = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    default = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    player = db.relationship('Player', back_populates='reductions')

    def __init__(self, playerId, reason, amount, default):
        self.playerId = playerId
        self.reason = reason
        self.amount = amount
        self.default = default

    def toDict(self):
        return {
            'id': self.id,
            'playerId': self.playerId,
            'reason': self.reason,
            'amount': self.amount,
            'default': self.default
        }

    def toDictForPlayer(self):
        return {
            'reason': self.reason,
            'amount': self.amount,
            'default': self.default
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            playerId=data['playerId'],
            reason=data['reason'],
            amount=data['amount'],
            default=data['default']
        )