from datetime import datetime
from database import db

class Profil(db.Model):
    __tablename__ = 'profils'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    value = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String, nullable=False)  
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)  
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  

    def __init__(self, label, value):
        self.label = label
        self.value = value

    def toDict(self):
        return {
            'id': self.id,
            'label': self.label,
            'value': self.value
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            label=data['label'],
            value=data['value']
        )