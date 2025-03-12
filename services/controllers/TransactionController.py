from flask import Blueprint, jsonify, request
from repositories.TransactionRepository import TransactionRepository
from models.Transaction import Transaction

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

    # Supprimer tous les transactions
    transactionRepository.deleteAllTransactions()

    # Ajouter les nouvelles transactions
    newTransactions = []
    for transactionData in transactions:
        newTransactions.append(Transaction(
            amount=transactionData['amount'],
            type=transactionData['type'],
            date=transactionData['date']
        ))

    transactionRepository.addTransactions(newTransactions)

    result = [transaction.toDict() for transaction in newTransactions]
    return jsonify(result), 200