from flask import Blueprint, jsonify, request
from models.Player import Player
from repositories.PlayerRepository import PlayerRepository

playerBp = Blueprint('playerBp', __name__, url_prefix='/players')

@playerBp.route('/', methods=['GET'])
def getPlayers():
    players = PlayerRepository.getAllPlayers()
    return jsonify([player.toDict() for player in players]), 200

@playerBp.route('/', methods=['POST'])
def addPlayer():
    player = Player.fromJson(request.json)
    PlayerRepository.addPlayer(player)
    return jsonify({"message": "Player added successfully!"}), 201

@playerBp.route('/multiple', methods=['POST'])
def addPlayers():
    players = []
    for player in request.json: 
        players.append(Player.fromJson(player))
    PlayerRepository.addPlayers(players)
    return jsonify({"message": "Players added successfully!"}), 201