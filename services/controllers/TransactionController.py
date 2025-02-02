from flask import Blueprint, jsonify, request
from repositories.TransactionRepository import TransactionRepository
from models.Transaction import Transaction
from database import db

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
    TransactionRepository.addTransactions(transactions)
    return jsonify({'message': 'Transactions added successfully!'}), 201


@transactionBp.route('/a', methods=['PUT'])
def updateTransaction():
    try:
        data = request.json
        transactions = data['transactions']
        if not isinstance(transactions, list):
            return jsonify({'error': 'Invalid transactions data format'}), 400
        
        # Supprimer tous les transactions
        Transaction.query.delete()

        # Ajouter les nouvelles transactions
        newTransactions = []
        for transactionData in transactions:
            newTransaction = Transaction(
                amount=transactionData['amount'],
                type=transactionData['type'],
                date=transactionData['date']
            )
            db.session.add(newTransaction)
            newTransactions.append(newTransaction)

        db.session.commit()

        result = [transaction.toDict() for transaction in newTransactions]
        return jsonify(result)

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': str(e)}), 500