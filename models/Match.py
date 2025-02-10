from datetime import datetime
from database import db

class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.Integer, nullable=False)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    double = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String, nullable=False)
    player1Id = db.Column(db.Integer, db.ForeignKey('players.id'))
    player2Id = db.Column(db.Integer, db.ForeignKey('players.id'))
    team1Id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team2Id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    player1Availability = db.Column(db.Integer)
    player2Availability = db.Column(db.Integer)
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

    #relashionship
    player1 = db.relationship('Player', foreign_keys=[player1Id], backref='player1')
    player2 = db.relationship('Player', foreign_keys=[player2Id], backref='player2')
    team1 = db.relationship('Team', foreign_keys=[team1Id], backref='team1')
    team2 = db.relationship('Team', foreign_keys=[team2Id], backref='team2')
    court = db.relationship('Court', backref='court')
    winner = db.relationship('Player', foreign_keys=[winnerId], backref='winner')

    def __init__(self, fftId, categoryId, double, label, player1Id, player2Id, team1Id, team2Id, player1Availability, player2Availability, day, hour, courtId, finish, winnerId, notif, score, panel, nextRound, calId, isActive):
        self.fftId = fftId
        self.categoryId = categoryId
        self.double = double
        self.label = label
        self.player1Id = player1Id
        self.player2Id = player2Id
        self.team1Id = team1Id
        self.team2Id = team2Id
        self.player1Availability = player1Availability
        self.player2Availability = player2Availability
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
            'double': self.double,
            'label': self.label,
            'player1Id': self.player1Id if self.double == 0 else self.team1Id,
            'player2Id': self.player2Id if self.double == 0 else self.team2Id,
            'player1Availability': self.player1Availability,
            'player2Availability': self.player2Availability,
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
            'player1' : self.player1.toMiniDict() if self.player1 else self.team1.toMiniDict() if self.team1 else None,
            'player2' : self.player2.toMiniDict() if self.player2 else self.team2.toMiniDict() if self.team2 else None,
            'court' : self.court.toDict() if self.court else None,
            'winner' : self.winner.toMiniDict() if self.winner else None
        }

    def getFormattedDate(self):
        day = self.day.split('-')
        if len(day) != 3 : return self.day
        return f"{day[2]}/{day[1]}"

    def getFormattedHour(self):
        return self.hour.replace(':', 'h')

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            categoryId=data['categoryId'],
            double=data['double'],
            label=data['label'],
            player1Id=data['player1Id'],
            player2Id=data['player2Id'],
            team1Id=data['team1Id'],
            team2Id=data['team2Id'],
            player1Availability=data['player1Availability'],
            player2Availability=data['player2Availability'],
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