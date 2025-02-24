from datetime import datetime
from database import db

class Competition(db.Model):
    __tablename__ = 'competitions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String, nullable=False)
    homologationId = db.Column(db.BigInteger, nullable=False)
    isActive = db.Column(db.Boolean, default=False, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, label, homologationId, isActive):
        self.label = label
        self.homologationId = homologationId
        self.isActive = isActive

    def toDict(self):
        return {
            'id': self.id,
            'label': self.label,
            'homologationId': self.homologationId,
            'isActive': self.isActive
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            label=data['label'],
            homologationId=data['homologationId'],
            isActive=data['isActive']
        )