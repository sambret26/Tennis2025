from datetime import datetime
from database import db

class Grid(db.Model):
    __tablename__ = 'grids'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.BigInteger, nullable=False)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    tableId = db.Column(db.BigInteger)
    nextGridId = db.Column(db.BigInteger)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = db.relationship('Category')

    def __init__(self, fftId, categoryId, name, type, tableId, nextGridId):
        self.fftId = fftId
        self.categoryId = categoryId
        self.name = name
        self.type = type
        self.tableId = tableId
        self.nextGridId = nextGridId

    def toDict(self):
        return {
            'id': self.id,
            'fftId': self.fftId,
            'categoryId': self.categoryId,
            'name': self.name,
            'type': self.type,
            'tableId': self.tableId,
            'nextGridId': self.nextGridId
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            categoryId=data['categoryId'],
            name=data['name'],
            type=data["type"],
            tableId=data["tableId"],
            nextGridId=data["nextGridId"]
        )

    @classmethod
    def fromFFT(cls, data):
        return cls(
            fftId=data['decoupageId'],
            categoryId=0,
            name=data['nomDecoupage'],
            type=data['typeDecoupage'],
            tableId=data['tableauActifId'],
            nextGridId=data['decoupageSuivantId']
        )
