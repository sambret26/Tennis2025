from flask import Blueprint, jsonify, request
from models.player import Player
from repositories.playerRepository import PlayerRepository

player_bp = Blueprint('player_bp', __name__, url_prefix='/players')

@player_bp.route('/', methods=['GET'])
def get_players():
    players = PlayerRepository.get_all_players()
    return jsonify([player.to_dict() for player in players]), 200

@player_bp.route('/', methods=['POST'])
def add_player():
    data = request.json
    player = Player(
        fft_id=data['fft_id'],
        inscription_id=data['inscription_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        ranking_id=data['ranking_id'],
        club=data['club'],
        state=data['state'],
        is_active=data['is_active']
    )
    PlayerRepository.add_player(player)
    return jsonify({"message": "Player added successfully!"}), 201