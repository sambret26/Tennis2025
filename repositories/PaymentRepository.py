from models.Payment import Payment
from database import db

class PaymentRepository:

    #GETTERS
    @staticmethod
    def getAllPayments():
        return Payment.query.all()

    @staticmethod
    def getAllPaymentsForPlayer(playerId):
        return Payment.query.filter_by(playerId=playerId).all()

    @staticmethod
    def getPaymentById(paymentId):
        return Payment.query.get(paymentId)

    @staticmethod
    def getAllPaymentsForDay(day):
        return Payment.query.filter_by(date=day).all()

    @staticmethod
    def getAllPaymentsBeforeDay(day):
        return Payment.query.filter(Payment.date < day).all()

    #ADDERS
    @staticmethod
    def addPayment(payment):
        db.session.add(payment)
        db.session.commit()

    @staticmethod
    def addPayments(payments):
        db.session.add_all(payments)
        db.session.commit()

    #DELETERS
    @staticmethod
    def deletePayment(payment):
        db.session.delete(payment)
        db.session.commit()

    @staticmethod
    def deleteAllPayments():
        Payment.query.delete()
        db.session.commit()

    @staticmethod
    def deleteAllPaymentsByPlayerId(playerId):
        Payment.query.filter_by(playerId=playerId).delete()
