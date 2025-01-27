from flask import Blueprint, jsonify, request
from repositories.ReductionRepository import ReductionRepository
from models.Reduction import Reduction
from database import db
from models.Player import Player
from models.PlayerBalance import PlayerBalance

reductionBp = Blueprint('reductionBp', __name__, url_prefix='/reductions')

@reductionBp.route('/', methods=['GET'])
def getReductions():
    reductions = ReductionRepository.getAllReductions()
    return jsonify([reduction.toDict() for reduction in reductions]), 200

@reductionBp.route('/', methods=['POST'])
def addReduction():
    reduction = Reduction.fromJson(request.json)
    ReductionRepository.addReduction(reduction)
    return jsonify({'message': 'Reduction added successfully!'}), 201

@reductionBp.route('/multiple', methods=['POST'])
def addReductions():
    reductions = []
    for data in request.json:
        reductions.append(Reduction.fromJson(data))
    ReductionRepository.addReductions(reductions)
    return jsonify({'message': 'Reductions added successfully!'}), 201

@reductionBp.route('/<int:playerId>', methods=['PUT'])
def updateReduction(playerId):
    try:
        player = Player.query.get(playerId)
        if not player:
            return jsonify({'error': 'Player not found'}), 404

        data = request.json
        reductions = data['reductions']
        balance = data['balance']
        if not isinstance(reductions, list):
            return jsonify({'error': 'Invalid reductions data format'}), 400
        
        # Supprimer tous les reductions existants du joueur
        Reduction.query.filter_by(playerId=playerId).delete()

        # Ajouter les nouveaux reductions
        new_reductions = []
        for reduction_data in reductions:
            new_reduction = Reduction(
                playerId=playerId,
                amount=reduction_data['amount'],
                reason=reduction_data['reason'],
                default=reduction_data['default']
            )
            db.session.add(new_reduction)
            new_reductions.append(new_reduction)

        # Mettre à jour la balance du joueur
        player_balance = PlayerBalance.query.filter_by(playerId=playerId).first()
        if player_balance:
            player_balance.remainingAmount = balance['remainingAmount']
            player_balance.finalAmount = balance['finalAmount']
            player_balance.initialAmount = balance['initialAmount']
            db.session.add(player_balance)

        db.session.commit()

        result = [reduction.toDict() for reduction in new_reductions]
        return jsonify(result)

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': str(e)}), 500