from flask import Blueprint, jsonify, request
from repositories.PlayerBalanceRepository import PlayerBalanceRepository
from models.PlayerBalance import PlayerBalance

playerBalanceBp = Blueprint('playerBalanceBp', __name__, url_prefix='/playerBalances')

@playerBalanceBp.route('/', methods=['GET'])
def getplayerBalances():
    playerBalances = PlayerBalanceRepository.getAllplayerBalances()
    return jsonify([playerBalance.toDict() for playerBalance in playerBalances]), 200

@playerBalanceBp.route('/', methods=['POST'])
def addplayerBalance():
    playerBalance = PlayerBalance.fromJson(request.json)
    PlayerBalanceRepository.addplayerBalance(playerBalance)
    return jsonify({'message': 'Player balance added successfully!'}), 201

@playerBalanceBp.route('/multiple', methods=['POST'])
def addplayerBalances():
    playerBalances = []
    for data in request.json:
        playerBalances.append(PlayerBalance.fromJson(data))
    for playerBalance in playerBalances:
        PlayerBalanceRepository.addplayerBalance(playerBalance)
    return jsonify({'message': 'Player balances added successfully!'}), 201