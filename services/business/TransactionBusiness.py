from flask import Blueprint, jsonify, request
from repositories.TransactionRepository import TransactionRepository
from models.Transaction import Transaction

transactionRepository = TransactionRepository()

transactionBp = Blueprint('transactionBp', __name__, url_prefix='/transactions')

def updateTransaction(transactions):
    transactionRepository.deleteAllTransactions()
    newTransactions = []
    for transactionData in transactions:
        newTransactions.append(Transaction(
            amount=transactionData['amount'],
            type=transactionData['type'],
            date=transactionData['date']
        ))
    transactionRepository.addTransactions(newTransactions)
    result = [transaction.toDict() for transaction in newTransactions]
    return result