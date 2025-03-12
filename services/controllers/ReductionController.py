from flask import Blueprint, jsonify, request
from repositories.PlayerRepository import PlayerRepository
from repositories.ReductionRepository import ReductionRepository
from repositories.PlayerBalanceRepository import PlayerBalanceRepository
from models.Reduction import Reduction
from services.business import ReductionBusiness

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
    result = ReductionBusiness.updateReduction(player, reductions, balance)
    return jsonify(result), 200