from flask import Blueprint, jsonify, request
from repositories.TransactionRepository import TransactionRepository
from models.Transaction import Transaction

transactionRepository = TransactionRepository()

transactionBp = Blueprint('transactionBp', __name__, url_prefix='/transactions')

@transactionBp.route('/', methods=['GET'])
def getTransactions():
    transactions = transactionRepository.getAllTransactions()
    return jsonify([transaction.toDict() for transaction in transactions]), 200

@transactionBp.route('/', methods=['POST'])
def addTransaction():
    transaction = Transaction.fromJson(request.json)
    transactionRepository.addTransaction(transaction)
    return jsonify({'message': 'Transaction added successfully!'}), 201

@transactionBp.route('/multiple', methods=['POST'])
def addTransactions():
    transactions = []
    for data in request.json:
        transactions.append(Transaction.fromJson(data))
    transactionRepository.addTransactions(transactions)
    return jsonify({'message': 'Transactions added successfully!'}), 201


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