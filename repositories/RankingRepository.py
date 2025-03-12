from models.Ranking import Ranking
from database import db

class RankingRepository:

    #GETTERS
    @staticmethod
    def getAllRankings():
        return Ranking.query.all()

    @staticmethod
    def getRankingById(rankingId):
        return Ranking.query.get(rankingId)

    @staticmethod
    def getRankingBySimple(rankingSimple):
        return Ranking.query.filter_by(simple=rankingSimple).first()

    @staticmethod
    def getRankingByDouble(rankingDouble):
        return Ranking.query.filter_by(double=rankingDouble).first()

    @staticmethod
    def getRankingMapSimple():
        return {r.simple: r for r in Ranking.query.all() if r.simple is not None}

    @staticmethod
    def getRankingMapDouble():
        return {r.double: r.id for r in Ranking.query.all() if r.double is not None}

    #ADDERS
    @staticmethod
    def addRanking(ranking):
        db.session.add(ranking)
        db.session.commit()

    @staticmethod
    def addRankings(rankings):
        db.session.add_all(rankings)
        db.session.commit()

    #DELETERS
    @staticmethod
    def deleteAllRankings():
        Ranking.query.delete()
        db.session.commit()