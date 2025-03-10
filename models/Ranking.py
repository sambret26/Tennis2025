from datetime import datetime
from database import db

class Ranking(db.Model):
    __tablename__ = 'rankings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.BigInteger, nullable=False)
    simple = db.Column(db.String, nullable=False)
    double = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    #players = db.relationship('Player', back_populates='ranking', lazy="select")
    #teams = db.relationship('Team', back_populates='ranking', lazy="select")

    def __init__(self, fftId, simple, double):
        self.fftId = fftId
        self.simple = simple
        self.double = double

    def toDict(self):
        return {
            'id': self.id,
            'fftId': self.fftId,
            'simple': self.simple,
            'double': self.double
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            simple=data['simple'],
            double=data['double']
        )

    @classmethod
    def fromFFT(cls, data):
        return cls(
            fftId=data['echelon'],
            simple=data['libelle'],
            double=0
        )