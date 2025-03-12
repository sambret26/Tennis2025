from flask import Blueprint, jsonify
from repositories.PlayerRepository import PlayerRepository

playerRepository = PlayerRepository()

playerBp = Blueprint('playerBp', __name__, url_prefix='/players')

@playerBp.route('/', methods=['GET'])
def getPlayers():
    players = playerRepository.getAllPlayers()
    return jsonify([player.toDict() for player in players]), 200