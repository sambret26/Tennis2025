from datetime import datetime
from database import db

class PlayerBalance(db.Model):
    __tablename__ = 'player_balances'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerId = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    initialAmount = db.Column(db.Integer, nullable=False)
    finalAmount = db.Column(db.Integer, nullable=False)
    remainingAmount = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, playerId, initialAmount, finalAmount, remainingAmount):
        self.playerId = playerId
        self.initialAmount = initialAmount
        self.finalAmount = finalAmount
        self.remainingAmount = remainingAmount

    def toDict(self):
        return {
            'id': self.id,
            'playerId': self.playerId,
            'initialAmount': self.initialAmount,
            'finalAmount': self.finalAmount,
            'remainingAmount': self.remainingAmount
        }

    def toDictForPlayer(self):
        return {
            'initialAmount': self.initialAmount,
            'finalAmount': self.finalAmount,
            'remainingAmount': self.remainingAmount
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            playerId=data['playerId'],
            initialAmount=data['initialAmount'],
            finalAmount=data['finalAmount'],
            remainingAmount=data['remainingAmount']
        )