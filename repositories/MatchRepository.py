from models.Match import Match
from database import db

class MatchRepository:

    #GETTERS
    @staticmethod
    def getMatchById(matchId):
        return Match.query.get(matchId)

    @staticmethod
    def getMatchesForPlanning(date):
        return Match.query.filter(Match.day == date).order_by(Match.hour, Match.courtId.asc()).all()

    @staticmethod
    def getMatchByLabel(matchLabel):
        return Match.query.filter(Match.label == matchLabel).first()

    @staticmethod
    def getMatchesMap():
        return {match.fftId: match for match in Match.query.all()}

    #ADDERS
    @staticmethod
    def addMatches(matches):
        db.session.add_all(matches)
        db.session.commit()

    #SETTERS
    @staticmethod
    def updateMatch(match):
        db.session.merge(match)
        db.session.commit()

    @staticmethod
    def updateMatchFromBatch(match):
        Match.query.filter_by(id=match.id).update({
            "label": match.label,
            "player1Id": match.player1Id,
            "player2Id": match.player2Id,
            "team1Id": match.team1Id,
            "team2Id": match.team2Id,
            "day": match.day,
            "hour": match.hour,
            "courtId": match.courtId,
            "finish": match.finish,
            "winnerId": match.winnerId,
            "teamWinnerId": match.teamWinnerId,
            "score": match.score,
            "nextRound": match.nextRound
        })
        db.session.commit()

    #DELETERS
    @staticmethod
    def deleteAllMatches():
        Match.query.delete()
        db.session.commit()

    @staticmethod
    def deleteMatches(matchsId):
        Match.query.filter(Match.id.in_(matchsId)).delete()
        db.session.commit()