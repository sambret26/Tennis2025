from models.Matches import Match
from database import db

class MatchRepository:

    @staticmethod
    def addMatch(match):
        db.session.add(match)
        db.session.commit()

    @staticmethod
    def getAllMatches():
        return Match.query.all()

    @staticmethod
    def getMatchById(matchId):
        return Match.query.get(matchId)