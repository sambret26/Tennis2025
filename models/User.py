from datetime import datetime
from database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    profileValue = db.Column(db.Integer, nullable=False)
    superAdmin = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.profileValue = 0
        self.superAdmin = 0

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'profileValue': self.profileValue,
            'superAdmin': self.superAdmin
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            name=data['username'],
            password=data['password']
        )