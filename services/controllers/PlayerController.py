from flask import Blueprint, jsonify, request
from models.Player import Player
from repositories.PlayerRepository import PlayerRepository

playerRepository = PlayerRepository()

playerBp = Blueprint('playerBp', __name__, url_prefix='/players')

@playerBp.route('/', methods=['GET'])
def getPlayers():
    players = playerRepository.getAllPlayers()
    return jsonify([player.toDict() for player in players]), 200

@playerBp.route('/allNames', methods=['GET'])
def getAllPlayerNames():
    players = playerRepository.getAllPlayerNames()
    return jsonify([player.toNameDict() for player in players]), 200
