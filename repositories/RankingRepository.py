from models.Ranking import Ranking
from database import db

class RankingRepository:

    #GETTERS
    @staticmethod
    def getAllRankings():
        return Ranking.query.all()

    @staticmethod
    def getRankingById(rankingId):
        return Ranking.query.get(rankingId).first()

    @staticmethod
    def getRankingBySimple(rankingSimple):
        return Ranking.query.filter_by(simple=rankingSimple).first()

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