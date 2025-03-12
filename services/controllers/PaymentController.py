from flask import Blueprint, jsonify, request
from repositories.PlayerRepository import PlayerRepository
from services.business import PaymentBusiness

paymentBp = Blueprint('PaymentBp', __name__, url_prefix='/payments')

playerRepository = PlayerRepository()

@paymentBp.route('/<int:playerId>', methods=['PUT'])
def updatePlayerPayments(playerId):
    player = playerRepository.getPlayerById(playerId)
    if not player:
        return jsonify({'error': 'Player not found'}), 404
    data = request.json
    payments = data['payments']
    balance = data['balance']
    if not isinstance(payments, list):
        return jsonify({'error': 'Invalid payments data format'}), 400
    result = PaymentBusiness.updatePayments(player, payments, balance)
    if result is None:
        return jsonify({'error': 'Player not found'}), 404
    return jsonify(result), 200