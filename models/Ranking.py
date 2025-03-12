from datetime import datetime
from database import db

class Ranking(db.Model):
    __tablename__ = 'rankings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.BigInteger, nullable=False)
    simple = db.Column(db.String)
    double = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    def fromFFTSimple(cls, data):
        return cls(
            fftId=data['echelon'],
            simple=data['libelle'],
            double=None
        )

    @classmethod
    def fromFFTDouble(cls, data):
        return cls(
            fftId=data['echelon'],
            simple=None,
            double=data['libelle']
        )