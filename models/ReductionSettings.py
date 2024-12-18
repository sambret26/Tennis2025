from datetime import datetime
from database import db

class ReductionSettings(db.Model):
    __tablename__ = 'reduction_settings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reason = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, reason, amount):
        self.reason = reason
        self.amount = amount

    def toDict(self):
        return {
            'id': self.id,
            'reason': self.reason,
            'amount': self.amount
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            reason=data['reason'],
            amount=data['amount']
        )