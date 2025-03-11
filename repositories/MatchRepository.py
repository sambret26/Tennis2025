from models.Match import Match
from database import db

class MatchRepository:

    #GETTERS
    @staticmethod
    def getMatchById(matchId):
        return Match.query.get(matchId)

    @staticmethod
    def getAllMatch():
        return Match.query.all()

    @staticmethod
    def getMatchesForPlanning(date):
        return Match.query.filter(Match.day == date).order_by(Match.hour, Match.courtId.asc()).all()

    @staticmethod
    def getMatchByLabel(matchLabel):
        return Match.query.filter(Match.label == matchLabel).first()

    @staticmethod
    def getAllMatchesIdByGrid(gridId):
        return [match.id for match in Match.query.filter(Match.gridId == gridId).all()]

    @staticmethod
    def getMatchByFftId(matchFftId):
        return Match.query.filter(Match.fftId == matchFftId).first()

    #ADDERS
    @staticmethod
    def addMatch(match):
        db.session.add(match)
        db.session.commit()

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
    def deleteAllMatchesByGrid(gridId):
        Match.query.filter(Match.gridId == gridId).delete()
        db.session.commit()

    @staticmethod
    def deleteAllMatches():
        Match.query.delete()
        db.session.commit()

    @staticmethod
    def deleteMatches(matchsId):
        Match.query.filter(Match.id.in_(matchsId)).delete()
        db.session.commit()
        db.session.commit()
        user = User.query.filter_by(id=userId).first()
        return user

    #DELETERS
    @staticmethod
    def deleteAllMatchesByGrid(gridId):
        Match.query.filter(Match.gridId == gridId).delete()
        db.session.commit()

    @staticmethod
    def deleteAllMatches():
        Match.query.delete()
        db.session.commit()

    @staticmethod
    def deleteMatches(matchsId):
        Match.query.filter(Match.id.in_(matchsId)).delete()
        db.session.commit()