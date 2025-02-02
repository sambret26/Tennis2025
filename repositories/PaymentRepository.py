from models.Payment import Payment
from database import db

class PaymentRepository:

    @staticmethod
    def addPayment(payment):
        db.session.add(payment)
        db.session.commit()

    @staticmethod
    def addPayments(payments):
        db.session.add_all(payments)
        db.session.commit()

    @staticmethod
    def getAllPayments():
        return Payment.query.all()

    @staticmethod
    def getPaymentById(Payment_id):
        return Payment.query.get(Payment_id)

    @staticmethod
    def getAllPaymentsForDay(day):
        return Payment.query.filter_by(date=day).all()

    @staticmethod
    def getAllPaymentsBeforeDay(day):
        return Payment.query.filter(Payment.date < day).all()