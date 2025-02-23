from datetime import datetime
from database import db

class Court(db.Model):
    __tablename__ = 'courts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.BigInteger, nullable=False)
    name = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #matches = db.relationship('Match', back_populates='court', lazy="select")

    def __init__(self, fftId, name, number):
        self.fftId = fftId
        self.name = name
        self.number = number

    def toDict(self):
        return {
            'id': self.id,
            'fftId': self.fftId,
            'name': self.name,
            'number': self.number
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            name=data['name'],
            number=data['number']
        )

    @classmethod
    def fromFFT(cls, data):
        return cls(
            fftId=data['courtId'],
            name=data['nom'],
            number=data['numero']
        )
