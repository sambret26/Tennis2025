from datetime import datetime
from database import db

class Availability(db.Model):
    __tablename__ = 'availabilities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, number, value):
        self.number = number
        self.value = value

    def toDict(self):
        return {
            'id': self.id,
            'number': self.number,
            'value': self.value
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            number=data['number'],
            value=data['value']
        )