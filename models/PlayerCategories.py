from datetime import datetime
from database import db

class PlayerCategories(db.Model):
    __tablename__ = 'player_categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerId = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, playerId, categoryId):
        self.playerId = playerId
        self.categoryId = categoryId

    def toDict(self):
        return {
            'id': self.id,
            'playerId': self.playerId,
            'categoryId': self.categoryId
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            playerId=data['playerId'],
            categoryId=data['categoryId']
        )