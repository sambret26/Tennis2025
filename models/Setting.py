from datetime import datetime
from database import db

class Setting(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def toDict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            key=data['key'],
            value=data['value']
        )