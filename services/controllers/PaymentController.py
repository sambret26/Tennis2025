from flask import Blueprint, jsonify, request
from repositories.PlayerBalanceRepository import PlayerBalanceRepository
from repositories.PaymentRepository import PaymentRepository
from repositories.PlayerRepository import PlayerRepository
from models.Payment import Payment

playerBalanceRepository = PlayerBalanceRepository()
paymentRepository = PaymentRepository()
playersRepository = PlayerRepository()

paymentBp = Blueprint('PaymentBp', __name__, url_prefix='/payments')

@paymentBp.route('/', methods=['GET'])
def getPayments():
    payments = paymentRepository.getAllPayments()
    return jsonify([payment.toDict() for payment in payments]), 200

@paymentBp.route('/', methods=['POST'])
def addPayment():
    payment = Payment.fromJson(request.json)
    paymentRepository.addPayment(payment)
    return jsonify({'message': 'Payment added successfully!'}), 201

@paymentBp.route('/<int:playerId>', methods=['PUT'])
def updatePlayerPayments(playerId):
    player = playersRepository.getPlayerById(playerId)
    if not player:
        return jsonify({'error': 'Player not found'}), 404

    data = request.json
    payments = data['payments']
    balance = data['balance']
    if not isinstance(payments, list):
        return jsonify({'error': 'Invalid payments data format'}), 400

    paymentRepository.deleteAllPaymentsByPlayerId(playerId)

    # Ajouter les nouveaux payments
    newPayments = []
    for paymentData in payments:
        newPayments.append(Payment(
            playerId=playerId,
            amount=paymentData['amount'],
            date=paymentData['date']
        ))

    paymentRepository.addPayments(newPayments)

    playerBalanceRepository.updatePlayerBalanceForPlayerId(playerId, balance)

    result = [payment.toDictForPlayer() for payment in newPayments]
    return jsonify(result), 200

@paymentBp.route('/<int:playerId>', methods=['GET'])
def getPlayerPayments(playerId):
    try:
        payments = paymentRepository.getAllPaymentsForPlayer(playerId)
        return jsonify([payment.toDictForPlayer() for payment in payments])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@paymentBp.route('/<int:paymentId>', methods=['DELETE'])
def deletePayment(paymentId):
    payment = paymentRepository.getPaymentById(paymentId)
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404

    # Récupérer le montant du payment et le playerId avant de le supprimer
    amount = payment.amount
    playerId = payment.playerId

    paymentRepository.deletePayment(payment)

    playerBalance = playerBalanceRepository.getPlayerBalanceByPlayerId(playerId)

    if playerBalance:
        playerBalance.remainingAmount = min(
            playerBalance.finalAmount,
            playerBalance.remainingAmount + amount
        )
    playerBalanceRepository.updatePlayerBalance(playerBalance)
    return jsonify({'message': 'Payment deleted successfully'})