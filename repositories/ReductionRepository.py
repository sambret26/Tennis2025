from models.Reduction import Reduction
from database import db

class ReductionRepository:

    @staticmethod
    def addReduction(reduction):
        db.session.add(reduction)
        db.session.commit()

    @staticmethod
    def getAllReductions():
        return Reduction.query.all()

    @staticmethod
    def getReductionById(reductionId):
        return Reduction.query.get(reductionId)