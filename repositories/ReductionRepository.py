from models.Reduction import Reduction
from database import db

class ReductionRepository:

    #GETTERS
    @staticmethod
    def getAllReductions():
        return Reduction.query.all()

    @staticmethod
    def getReductionById(reductionId):
        return Reduction.query.get(reductionId)

    #ADDERS
    @staticmethod
    def addReduction(reduction):
        db.session.add(reduction)
        db.session.commit()

    @staticmethod
    def addReductions(reductions):
        db.session.add_all(reductions)
        db.session.commit()

    #DELETERS
    @staticmethod
    def deleteReduction(reduction):
        db.session.delete(reduction)
        db.session.commit()

    @staticmethod
    def deleteAllReductions():
        Reduction.query.delete()
        db.session.commit()

    @staticmethod
    def deleteAllReductionsByPlayerId(playerId):
        Reduction.query.filter_by(playerId=playerId).delete()