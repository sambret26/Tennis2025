from models.Match import Match
from database import db

class MatchRepository:

    @staticmethod
    def addMatch(match):
        db.session.add(match)
        db.session.commit()

    @staticmethod
    def addMatches(matches):
        db.session.addAll(matches)
        db.session.commit()

    @staticmethod
    def getAllMatch():
        return Match.query.all()

    @staticmethod
    def getMatchById(matchId):
        return Match.query.get(matchId)