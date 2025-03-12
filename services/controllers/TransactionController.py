from flask import Blueprint, jsonify, request
from repositories.TransactionRepository import TransactionRepository
from services.business import TransactionBusiness

transactionRepository = TransactionRepository()

transactionBp = Blueprint('transactionBp', __name__, url_prefix='/transactions')

@transactionBp.route('/', methods=['GET'])
def getTransactions():
    transactions = transactionRepository.getAllTransactions()
    return jsonify([transaction.toDict() for transaction in transactions]), 200

@transactionBp.route('/', methods=['PUT'])
def updateTransaction():
    data = request.json
    transactions = data['transactions']
    if not isinstance(transactions, list):
        return jsonify({'error': 'Invalid transactions data format'}), 400
    result = TransactionBusiness.updateTransaction(transactions)
    return jsonify(result), 200