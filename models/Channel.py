from datetime import datetime
from database import db

class Channel(db.Model):
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String)
    channelId = db.Column(db.BigInteger)
    type = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, category, channelId, type):
        self.category = category
        self.channelId = channelId
        self.type = type

    def toDict(self):
        return {
            'id': self.id,
            'category': self.category,
            'channelId': self.channelId,
            'type': self.type
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            category=data['category'],
            channelId=data['channelId'],
            type=data['type']
        )