from flask import Blueprint, jsonify, request
from repositories.PlayerRepository import PlayerRepository
from repositories.ReductionRepository import ReductionRepository
from repositories.PlayerBalanceRepository import PlayerBalanceRepository
from models.Reduction import Reduction

playerRepository = PlayerRepository()
reductionRepository = ReductionRepository()
playerBalanceRepository = PlayerBalanceRepository()

reductionBp = Blueprint('reductionBp', __name__, url_prefix='/reductions')

@reductionBp.route('/', methods=['GET'])
def getReductions():
    reductions = reductionRepository.getAllReductions()
    return jsonify([reduction.toDict() for reduction in reductions]), 200

@reductionBp.route('/', methods=['POST'])
def addReduction():
    reduction = Reduction.fromJson(request.json)
    reductionRepository.addReduction(reduction)
    return jsonify({'message': 'Reduction added successfully!'}), 201

@reductionBp.route('/<int:playerId>', methods=['PUT'])
def updateReduction(playerId):
    player = playerRepository.getPlayerById(playerId)
    if not player:
        return jsonify({'error': 'Player not found'}), 404

    data = request.json
    reductions = data['reductions']
    balance = data['balance']
    if not isinstance(reductions, list):
        return jsonify({'error': 'Invalid reductions data format'}), 400

    reductionRepository.deleteAllReductionsByPlayerId(playerId)

    # Ajouter les nouveaux reductions
    newReductions = []
    for reductionData in reductions:
        newReductions.append(Reduction(
            playerId=playerId,
            amount=reductionData['amount'],
            reason=reductionData['reason'],
            default=reductionData['default']
        ))

    reductionRepository.addReductions(newReductions)

    playerBalanceRepository.updatePlayerBalanceForPlayerId(playerId, balance)

    result = [reduction.toDict() for reduction in new_reductions]
    return jsonify(result), 200