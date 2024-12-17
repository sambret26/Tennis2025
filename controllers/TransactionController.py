from flask import Blueprint, jsonify, request
from repositories.TransactionRepository import TransactionRepository
from models.Transaction import Transaction

transactionBp = Blueprint('transactionBp', __name__, url_prefix='/transactions')

@transactionBp.route('/', methods=['GET'])
def getTransactions():
    transactions = TransactionRepository.getAllTransactions()
    return jsonify([transaction.toDict() for transaction in transactions]), 200

@transactionBp.route('/', methods=['POST'])
def addTransaction():
    transaction = Transaction.fromJson(request.json)
    TransactionRepository.addTransaction(transaction)
    return jsonify({'message': 'Transaction added successfully!'}), 201

@transactionBp.route('/multiple', methods=['POST'])
def addTransactions():
    transactions = []
    for data in request.json:
        transactions.append(Transaction.fromJson(data))
    for transaction in transactions:
        TransactionRepository.addTransaction(transaction)
    return jsonify({'message': 'Transactions added successfully!'}), 201