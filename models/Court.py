from datetime import datetime
from database import db

class Court(db.Model):
    __tablename__ = 'courts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, fftId, name):
        self.fftId = fftId
        self.name = name

    def toDict(self):
        return {
            'id': self.id,
            'fftId': self.fftId,
            'name': self.name,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            name=data['name']
        )
