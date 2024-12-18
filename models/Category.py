from datetime import datetime
from database import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False)
    label = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, code, label, amount):
        self.code = code
        self.label = label
        self.amount = amount

    def toDict(self):
        return {
            'id': self.id,
            'code': self.code,
            'label': self.label,
            'amount': self.amount
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            code=data['code'],
            label=data['label'],
            amount=data['amount']
        )