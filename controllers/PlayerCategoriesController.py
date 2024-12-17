from flask import Blueprint, jsonify, request
from repositories.PlayerCategoriesRepository import PlayerCategoriesRepository
from models.PlayerCategories import PlayerCategories

playerCategoriesBp = Blueprint('playerCategoriesBp', __name__, url_prefix='/playerCategories')

@playerCategoriesBp.route('/', methods=['GET'])
def getplayerCategories():
    playerCategories = PlayerCategoriesRepository.getAllplayerCategories()
    return jsonify([playerCategory.toDict() for playerCategory in playerCategories]), 200

@playerCategoriesBp.route('/', methods=['POST'])
def addPlayerCategory():
    playerCategory = PlayerCategories.fromJson(request.json)
    PlayerCategoriesRepository.addPlayerCategory(playerCategory)
    return jsonify({'message': 'Player category added successfully!'}), 201

@playerCategoriesBp.route('/multiple', methods=['POST'])
def addPlayerCategories():
    playerCategories = []
    for data in request.json:
        playerCategories.append(PlayerCategories.fromJson(data))
    for playerCategory in playerCategories:
        PlayerCategoriesRepository.addPlayerCategory(playerCategory)
    return jsonify({'message': 'Player categories added successfully!'}), 201