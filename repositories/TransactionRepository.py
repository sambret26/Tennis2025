from models.Transaction import Transaction
from database import db

class TransactionRepository:

    @staticmethod
    def addTransaction(transaction):
        db.session.add(transaction)
        db.session.commit()

    @staticmethod
    def addTransactions(transactions):
        db.session.add_all(transactions)
        db.session.commit()

    @staticmethod
    def getAllTransactions():
        return Transaction.query.order_by(Transaction.date).all()

    @staticmethod
    def getTransactionById(transactionId):
        return Transaction.query.get(transactionId)

    @staticmethod
    def getAllTransactionBeforeDay(day):
        return Transaction.query.filter(Transaction.date<day).all()

    @staticmethod
    def getAllWithdrawalForDay(day):
        return Transaction.query.filter_by(date=day, type=0).all()

    @staticmethod
    def deleteAllTransactions():
        Transaction.query.delete()
        db.session.commit()