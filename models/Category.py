from datetime import datetime
from database import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.BigInteger, unique=True, index=True)
    code = db.Column(db.String, nullable=False)
    label = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #grids = db.relationship('Grid', back_populates='category', lazy="select")
    #matches = db.relationship('Match', back_populates='category', lazy="select")

    def __init__(self, fftId, code, label, amount):
        self.fftId = fftId
        self.code = code
        self.label = label
        self.amount = amount

    def toDict(self):
        return {
            'id': self.id,
            'fftId': self.fftId,
            'code': self.code,
            'label': self.label,
            'amount': self.amount
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            code=data['code'],
            label=data['label'],
            amount=data['amount']
        )

    @classmethod
    def fromFFT(cls, data):
        return cls(
            fftId=data['epreuveId'],
            code=data['libelle'][:2],
            label=data['libelle'],
            amount=0
        )