from datetime import datetime
from database import db

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String)
    message = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, category, message):
        self.category = category
        self.message = message

    def toDict(self):
        return {
            'id': self.id,
            'category': self.category,
            'message': self.message
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            category=data['category'],
            message=data['message']
        )