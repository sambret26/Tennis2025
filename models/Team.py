from datetime import datetime
from database import db

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.BigInteger, nullable=False)
    player1Id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    player2Id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    rankingId = db.Column(db.Integer, db.ForeignKey('rankings.id'), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #relashionship
    player1 = db.relationship('Player', foreign_keys=[player1Id])
    player2 = db.relationship('Player', foreign_keys=[player2Id])
    ranking = db.relationship('Ranking')

    def __init__(self, fftId, player1Id, player2Id, rankingId):
        self.fftId = fftId
        self.player1Id = player1Id
        self.player2Id = player2Id
        self.rankingId = rankingId

    def toDict(self):
        return {
            'id': self.id,
            'fftId': self.fftId,
            'player1Id': self.player1Id,
            'player2Id': self.player2Id,
            'rankingId': self.rankingId
        }

    def toMiniDict(self):
        return {
            "id": self.id,
            "fullName": self.getFullName(),
            "ranking": self.ranking.double,
            "player1": self.player1.toMiniDict(),
            "player2": self.player2.toMiniDict()
        }

    def getFullName(self):
        return f"{self.player1.lastName.upper()}/{self.player2.lastName.upper()}"

    def getFullNameWithRanking(self):
        return f"{self.getFullName()} ({self.ranking.double})"

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            player1Id=data['player1Id'],
            player2Id=data['player2Id'],
            rankingId=data['rankingId']
        )