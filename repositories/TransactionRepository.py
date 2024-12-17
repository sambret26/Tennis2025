from models.Transaction import Transaction
from database import db

class TransactionRepository:

    @staticmethod
    def addTransaction(transaction):
        db.session.add(transaction)
        db.session.commit()

    @staticmethod
    def getAllTransactions():
        return Transaction.query.all()

    @staticmethod
    def getTransactionById(transactionId):
        return Transaction.query.get(transactionId)