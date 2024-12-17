from datetime import datetime
from database import db

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    fftId = db.Column(db.Integer, nullable=False)  
    player1Id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)  
    player2Id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)  
    rankingId = db.Column(db.Integer, db.ForeignKey('rankings.id'), nullable=False)  
    state = db.Column(db.Integer, nullable=False)  
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)  
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  

    def __init__(self, fftId, player1Id, player2Id, rankingId, state):
        self.fftId = fftId
        self.player1Id = player1Id
        self.player2Id = player2Id
        self.rankingId = rankingId
        self.state = state

    def toDict(self):
        return {
            'id': self.id,
            'fftId': self.fftId,
            'player1Id': self.player1Id,
            'player2Id': self.player2Id,
            'rankingId': self.rankingId,
            'state': self.state,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            player1Id=data['player1Id'],
            player2Id=data['player2Id'],
            rankingId=data['rankingId'],
            state=data['state']
        )