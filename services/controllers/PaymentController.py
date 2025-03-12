from flask import Blueprint, jsonify, request
from repositories.PlayerBalanceRepository import PlayerBalanceRepository
from repositories.PaymentRepository import PaymentRepository
from repositories.PlayerRepository import PlayerRepository
from models.Payment import Payment

playerBalanceRepository = PlayerBalanceRepository()
paymentRepository = PaymentRepository()
playersRepository = PlayerRepository()

paymentBp = Blueprint('PaymentBp', __name__, url_prefix='/payments')

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