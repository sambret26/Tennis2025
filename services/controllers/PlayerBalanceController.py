from flask import Blueprint, jsonify, request
from repositories.PlayerBalanceRepository import PlayerBalanceRepository
from models.PlayerBalance import PlayerBalance

playerBalanceRepository = PlayerBalanceRepository()

playerBalanceBp = Blueprint('playerBalanceBp', __name__, url_prefix='/playerBalances')

@playerBalanceBp.route('/', methods=['GET'])
def getplayerBalances():
    playerBalances = playerBalanceRepository.getAllplayerBalances()
    return jsonify([playerBalance.toDict() for playerBalance in playerBalances]), 200

@playerBalanceBp.route('/', methods=['POST'])
def addplayerBalance():
    playerBalance = PlayerBalance.fromJson(request.json)
    playerBalanceRepository.addplayerBalance(playerBalance)
    return jsonify({'message': 'Player balance added successfully!'}), 201
