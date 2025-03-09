from datetime import datetime
from database import db

class Competition(db.Model):
    __tablename__ = 'competitions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String, nullable=False)
    isActive = db.Column(db.Boolean, nullable=False, default=True)
    homologationId = db.Column(db.BigInteger, nullable=False)
    startDate = db.Column(db.String)
    endDate = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, label, isActive, homologationId, startDate, endDate):
        self.label = label
        self.isActive = isActive
        self.homologationId = homologationId
        self.startDate = startDate
        self.endDate = endDate

    def isDifferent(self, competition):
        return self.label != competition.label or \
            self.startDate != competition.startDate or \
            self.endDate != competition.endDate

    def toDict(self):
        return {
            'id': self.id,
            'label': self.label,
            'isActive': self.isActive,
            'homologationId': self.homologationId,
            'startDate': self.startDate,
            'endDate': self.endDate,
        }

    def toDictForDB(self):
        return {
            'label': self.label,
            'homologationId': self.homologationId,
            'startDate': self.startDate,
            'endDate': self.endDate
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            label=data['label'],
            isActive = data['isActive'],
            homologationId=data['homologationId'],
            startDate=data['startDate'],
            endDate=data['endDate']
        )

    @classmethod
    def fromFFT(cls, data):
        return cls(
            label=data['competitionNom'],
            isActive = 0,
            homologationId=data['homologationId'],
            startDate=data['dateDebutHomologation'].split('T')[0],
            endDate=data['dateFinHomologation'].split('T')[0]
        )