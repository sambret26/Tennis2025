from datetime import datetime
from database import db

class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.Integer, nullable=False)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    label = db.Column(db.String, nullable=False)
    player1Id = db.Column(db.Integer, db.ForeignKey('players.id'))
    player2Id = db.Column(db.Integer, db.ForeignKey('players.id'))
    day = db.Column(db.String)
    hour = db.Column(db.String)
    courtId = db.Column(db.Integer, db.ForeignKey('courts.id'))
    finish = db.Column(db.Integer, nullable=False)
    winnerId = db.Column(db.Integer, db.ForeignKey('players.id'))
    notif = db.Column(db.Integer, nullable=False)
    score = db.Column(db.String)
    panel = db.Column(db.String)
    nextRound = db.Column(db.String)
    calId = db.Column(db.String)
    isActive = db.Column(db.Boolean, default=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, fftId, categoryId, label, player1Id, player2Id, day, hour, courtId, finish, winnerId, notif, score, panel, nextRound, calId, isActive):
        self.fftId = fftId
        self.categoryId = categoryId
        self.label = label
        self.player1Id = player1Id
        self.player2Id = player2Id
        self.day = day
        self.hour = hour
        self.courtId = courtId
        self.finish = finish
        self.winnerId = winnerId
        self.notif = notif
        self.score = score
        self.panel = panel
        self.nextRound = nextRound
        self.calId = calId
        self.isActive = isActive

    def toDict(self):
        return {
            'id': self.id,
            'fftId': self.fftId,
            'categoryId': self.categoryId,
            'label': self.label,
            'player1Id': self.player1Id,
            'player2Id': self.player2Id,
            'day': self.day,
            'hour': self.hour,
            'courtId': self.courtId,
            'finish': self.finish,
            'winnerId': self.winnerId,
            'notif': self.notif,
            'score': self.score,
            'panel': self.panel,
            'nextRound': self.nextRound,
            'calId': self.calId,
            'isActive': self.isActive,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            categoryId=data['categoryId'],
            label=data['label'],
            player1Id=data['player1Id'],
            player2Id=data['player2Id'],
            day=data['day'],
            hour=data['hour'],
            courtId=data['courtId'],
            finish=data['finish'],
            winnerId=data['winnerId'],
            notif=data['notif'],
            score=data['score'],
            panel=data['panel'],
            nextRound=data['nextRound'],
            calId=data['calId'],
            isActive=data['isActive']
        )