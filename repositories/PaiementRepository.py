from models.Paiement import Paiement
from database import db

class PaiementRepository:

    @staticmethod
    def addPaiement(paiement):
        db.session.add(paiement)
        db.session.commit()

    @staticmethod
    def addPaiements(paiements):
        db.session.add_all(paiements)
        db.session.commit()

    @staticmethod
    def getAllPaiements():
        return Paiement.query.all()

    @staticmethod
    def getPaiementById(paiement_id):
        return Paiement.query.get(paiement_id)