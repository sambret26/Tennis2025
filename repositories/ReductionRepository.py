from models.Reduction import Reduction
from database import db

class ReductionRepository:

    @staticmethod
    def addReduction(reduction):
        db.session.add(reduction)
        db.session.commit()

    @staticmethod
    def addReductions(reductions):
        db.session.addAll(reductions)
        db.session.commit()

    @staticmethod
    def getAllReductions():
        return Reduction.query.all()

    @staticmethod
    def getReductionById(reductionId):
        return Reduction.query.get(reductionId)

    @staticmethod
    def updateReductions(playerId, reductions_data):
        # Récupérer les réductions existantes pour le joueur
        reductions = Reduction.query.filter_by(playerId=playerId).all()
        
        # Mettre à jour les réductions
        for reduction in reductions:
            # Ici, vous pouvez mettre à jour les propriétés de la réduction selon les données reçues
            # Par exemple, si vous avez un champ 'amount' dans le modèle Reduction
            reduction.amount = reductions_data.get('amount', reduction.amount)
        
        db.session.commit()
        return True