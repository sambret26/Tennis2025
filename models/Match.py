from datetime import datetime
from database import db

class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fftId = db.Column(db.BigInteger, nullable=False, index=True)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    gridId = db.Column(db.Integer, db.ForeignKey('grids.id'), nullable=False, index=True)
    double = db.Column(db.Boolean, nullable=False, default=False)
    label = db.Column(db.String)
    player1Id = db.Column(db.Integer, db.ForeignKey('players.id'))
    player2Id = db.Column(db.Integer, db.ForeignKey('players.id'))
    team1Id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team2Id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    player1Availability = db.Column(db.Integer)
    player2Availability = db.Column(db.Integer)
    day = db.Column(db.String)
    hour = db.Column(db.String)
    courtId = db.Column(db.Integer, db.ForeignKey('courts.id'))
    finish = db.Column(db.Boolean, nullable=False, default=False)
    winnerId = db.Column(db.Integer, db.ForeignKey('players.id'))
    teamWinnerId = db.Column(db.Integer, db.ForeignKey('teams.id'))
    notif = db.Column(db.Boolean, nullable=False, default=False)
    score = db.Column(db.String)
    nextRound = db.Column(db.String)
    calId = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #Relationship
    category = db.relationship('Category')
    player1 = db.relationship('Player', foreign_keys=[player1Id])
    player2 = db.relationship('Player', foreign_keys=[player2Id])
    team1 = db.relationship('Team', foreign_keys=[team1Id])
    team2 = db.relationship('Team', foreign_keys=[team2Id])
    court = db.relationship('Court')
    winner = db.relationship('Player', foreign_keys=[winnerId])
    teamWinner = db.relationship('Team', foreign_keys=[teamWinnerId])
    grid = db.relationship('Grid')

    def __init__(self, fftId, label=None, categoryId=None, gridId=None,\
        double=False, player1Id=None, player2Id=None, team1Id=None, team2Id=None,\
        player1Availability=0, player2Availability=0, day=None,\
        hour=None, courtId=None, finish=False, winnerId=None, teamWinnerId=None,\
        notif=False, score="", nextRound=None, calId=None):
        self.fftId = fftId
        self.categoryId = categoryId
        self.gridId = gridId
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
        self.teamWinnerId = teamWinnerId
        self.notif = notif
        self.score = score
        self.nextRound = nextRound
        self.calId = calId

    def toDict(self):
        return {
            'id': self.id,
            'fftId': self.fftId,
            'categoryId': self.categoryId,
            'gridId': self.gridId,
            'double': self.double,
            'label': self.label,
            'player1Id': self.player1Id if not self.double else self.team1Id,
            'player2Id': self.player2Id if not self.double else self.team2Id,
            'player1Availability': self.player1Availability,
            'player2Availability': self.player2Availability,
            'day': self.day,
            'hour': self.hour,
            'courtId': self.courtId,
            'finish': self.finish,
            'winnerId': self.winnerId if not self.double else self.teamWinnerId,
            'notif': self.notif,
            'score': self.score,
            'nextRound': self.nextRound,
            'calId': self.calId,
            'player1' : self.getPlayer1ForMiniDict(),
            'player2' : self.getPlayer2ForMiniDict(),
            'court' : self.court.toDict() if self.court else None,
            'winner' : self.getWinnerForMiniDict()
        }

    def getFormattedDate(self):
        day = self.day.split('-')
        if len(day) != 3 :
            return self.day
        return f"{day[2]}/{day[1]}"

    def getFormattedHour(self):
        return self.hour.replace(':', 'h')

    def getPlayer1ForMiniDict(self):
        if self.player1:
            return self.player1.toMiniDict()
        if self.team1:
            return self.team1.toMiniDict()
        return None

    def getPlayer2ForMiniDict(self):
        if self.player2:
            return self.player2.toMiniDict()
        if self.team2:
            return self.team2.toMiniDict()
        return None

    def getWinnerForMiniDict(self):
        if self.winner:
            return self.winner.toMiniDict()
        if self.teamWinner:
            return self.teamWinner.toMiniDict()
        return None

    @classmethod
    def fromJson(cls, data):
        return cls(
            fftId=data['fftId'],
            categoryId=data['categoryId'],
            gridId=data['gridId'],
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
            teamWinnerId=data['teamWinnerId'],
            notif=data['notif'],
            score=data['score'],
            nextRound=data['nextRound'],
            calId=data['calId']
        )

    @classmethod
    def fromFFT(cls, data):
        return cls(
            fftId=data['matchId'],
            nextRound=data['matchsSuivants']['matchId'] if 'matchId' in data['matchsSuivants'] else None
        )

    def isDifferent(self, match):
        if self.label != match.label or \
            self.player1Id != match.player1Id or \
            self.player2Id != match.player2Id or \
            self.team1Id != match.team1Id or \
            self.team2Id != match.team2Id or \
            self.day != match.day or \
            self.hour != match.hour or \
            self.courtId != match.courtId or \
            self.finish != match.finish or \
            self.winnerId != match.winnerId or \
            self.teamWinnerId != match.teamWinnerId or \
            self.score != match.score or \
            self.nextRound != match.nextRound or \
            self.calId != match.calId:
            return True
        return False