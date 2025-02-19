from models.Match import Match
from database import db

class MatchRepository:

    @staticmethod
    def addMatch(match):
        db.session.add(match)
        db.session.commit()

    @staticmethod
    def addMatches(matches):
        db.session.add_all(matches)
        db.session.commit()

    @staticmethod
    def updateMatch(match):
        db.session.merge(match)
        db.session.commit()

    @staticmethod
    def getAllMatch():
        return Match.query.all()

    @staticmethod
    def getMatchById(matchId):
        return Match.query.get(matchId)

    @staticmethod
    def getMatchesForPlanning(date):
        return Match.query.filter(Match.day == date).order_by(Match.hour).all()

    @staticmethod
    def getMatchByLabel(matchLabel):
        return Match.query.filter(Match.label == matchLabel).first()

    @staticmethod
    def deleteAllMatchesByGrid(gridId):
        Match.query.filter(Match.gridId == gridId).delete()
        db.session.commit()