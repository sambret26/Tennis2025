from models.Ranking import Ranking
from database import db

class RankingRepository:

    @staticmethod
    def addRanking(ranking):
        db.session.add(ranking)
        db.session.commit()

    @staticmethod
    def getAllRankings():
        return Ranking.query.all()

    @staticmethod
    def getRankingById(rankingId):
        return Ranking.query.get(rankingId)