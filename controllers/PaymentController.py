from flask import Blueprint, jsonify, request
from repositories.PaymentRepository import PaymentRepository
from models.Payment import Payment
from database import db
from models.Player import Player
from models.PlayerBalance import PlayerBalance

paymentBp = Blueprint('PaymentBp', __name__, url_prefix='/payments')

@paymentBp.route('/', methods=['GET'])
def getPayments():
    payments = PaymentRepository.getAllPayments()
    return jsonify([payment.toDict() for payment in payments]), 200

@paymentBp.route('/', methods=['POST'])
def addPayment():
    payment = Payment.fromJson(request.json)
    PaymentRepository.addPayment(payment)
    return jsonify({'message': 'Payment added successfully!'}), 201

@paymentBp.route('/multiple', methods=['POST'])
def addPayments():
    payments = []
    for data in request.json:
        payments.append(Payment.fromJson(data))
    PaymentRepository.addPayments(payments)
    return jsonify({'message': 'Payments added successfully!'}), 201

@paymentBp.route('/<int:playerId>', methods=['PUT'])
def update_player_payments(playerId):
    try:
        player = Player.query.get(playerId)
        if not player:
            return jsonify({'error': 'Player not found'}), 404

        data = request.json
        payments = data['payments']
        balance = data['balance']
        if not isinstance(payments, list):
            return jsonify({'error': 'Invalid payments data format'}), 400

        # Supprimer tous les payments existants du joueur
        Payment.query.filter_by(playerId=playerId).delete()

        # Ajouter les nouveaux payments
        new_payments = []
        for payment_data in payments:
            new_payment = Payment(
                playerId=playerId,
                amount=payment_data['amount'],
                date=payment_data['date']
            )
            db.session.add(new_payment)
            new_payments.append(new_payment)


        # Mettre à jour la balance du joueur si nécessaire
        player_balance = PlayerBalance.query.filter_by(playerId=playerId).first()
        if player_balance:
            player_balance.remainingAmount = balance['remainingAmount']
            player_balance.finalAmount = balance['finalAmount']
            player_balance.initialAmount = balance['initialAmount']
            db.session.add(player_balance)

        db.session.commit()

        result = [payment.toDictForPlayer() for payment in new_payments]
        return jsonify(result)

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@paymentBp.route('/<int:playerId>', methods=['GET'])
def get_player_payments(playerId):
    try:
        payments = Payment.query.filter_by(playerId=playerId).all()
        return jsonify([payment.toDictForPlayer() for payment in payments])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@paymentBp.route('/<int:paymentId>', methods=['DELETE'])
def delete_payment(paymentId):
    try:
        payment = Payment.query.get(paymentId)
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404

        # Récupérer le montant du payment et le playerId avant de le supprimer
        amount = payment.amount
        playerId = payment.playerId

        db.session.delete(payment)

        # Mettre à jour la balance du joueur
        player_balance = PlayerBalance.query.filter_by(playerId=playerId).first()
        if player_balance:
            player_balance.remainingAmount = min(
                player_balance.finalAmount,
                player_balance.remainingAmount + amount
            )
            db.session.add(player_balance)

        db.session.commit()
        return jsonify({'message': 'Payment deleted successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500