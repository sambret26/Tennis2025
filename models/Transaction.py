from datetime import datetime
from database import db

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    type = db.Column(db.Integer, nullable=False)  
    amount = db.Column(db.Integer, nullable=False)  
    date = db.Column(db.String, nullable=False)  
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)  
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  

    def __init__(self, type, amount, date):
        self.type = type
        self.amount = amount
        self.date = date

    def toDict(self):
        return {
            'type': self.type,
            'amount': self.amount,
            'date': self.date
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            type=data['type'],
            amount=data['amount'],
            date=data['date']
        )