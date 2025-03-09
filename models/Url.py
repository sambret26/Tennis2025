from datetime import datetime
from database import db

class Url(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String)
    url = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, label, url):
        self.label = label
        self.url = url

    def toDict(self):
        return {
            'id': self.id,
            'label': self.label,
            'url': self.url
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            label=data['label'],
            url=data['url']
        )