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
        matches = Match.query.with_entities(Match.fftId, Match.id, Match.label, Match.player1Id, Match.player2Id, Match.team1Id, Match.team2Id, Match.day, Match.hour, Match.courtId, Match.finish, Match.winnerId, Match.teamWinnerId, Match.score, Match.nextRound, Match.calId).all()
        return {match.fftId: match for match in matches}

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