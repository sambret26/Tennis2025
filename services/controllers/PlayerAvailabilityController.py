from flask import Blueprint, jsonify, request
from repositories import PlayerRepository
from repositories.PlayerAvailabilityRepository import PlayerAvailabilityRepository
from models.PlayerAvailability import PlayerAvailability

playerAvailabilityBp = Blueprint('playerAvailabilityBp', __name__, url_prefix='/playerAvailabilities')

@playerAvailabilityBp.route('/all', methods=['GET'])
def getPlayerAvailabilities():
    playerAvailabilities = PlayerAvailabilityRepository.getAllPlayerAvailabilities()
    return jsonify([playerAvailability.toDict() for playerAvailability in playerAvailabilities]), 200

@playerAvailabilityBp.route('/player/<int:playerId>', methods=['GET'])
def getPlayerAvailabilitiesByPlayerId(playerId):
    playerAvailabilities = PlayerAvailabilityRepository.getPlayerAvailabilityByPlayerId(playerId)
    return jsonify([playerAvailability.toDict() for playerAvailability in playerAvailabilities]), 200

@playerAvailabilityBp.route('/date', methods=['GET'])
def getAvailabilitiesForDay():
    date = request.args.get('date')
    playerAvailabilities = PlayerAvailabilityRepository.getPlayerAvailabilityByDay(date)
    return jsonify([playerAvailability.toDict() for playerAvailability in playerAvailabilities]), 200

@playerAvailabilityBp.route('/', methods=['POST'])
def addPlayerAvailability():
    playerAvailability = PlayerAvailability.fromJson(request.json)
    PlayerAvailabilityRepository.addPlayerAvailability(playerAvailability)
    return jsonify({'message': 'PlayerAvailability added successfully!'}), 201

@playerAvailabilityBp.route('/update', methods=['POST'])
def updatePlayerAvailability():
    playerAvailability = PlayerAvailability.fromJson(request.json)
    result = PlayerAvailabilityRepository.getPlayerAvailabilityIdByPlayerIdDayTimeSlot(playerAvailability.playerId, playerAvailability.day, playerAvailability.timeSlot)
    id = result[0] if result else None
    if id:
        PlayerAvailabilityRepository.updatePlayerAvailability(id, playerAvailability.available)
        return jsonify({'message': 'PlayerAvailability created successfully!'}), 200
    PlayerAvailabilityRepository.addPlayerAvailability(playerAvailability)
    return jsonify({'message': 'PlayerAvailability updated successfully!'}), 200

@playerAvailabilityBp.route('/multiple', methods=['POST'])
def addPlayerAvailabilities():
    playerAvailabilities = []
    for data in request.json:
        playerAvailabilities.append(PlayerAvailability.fromJson(data))
    PlayerAvailabilityRepository.addPlayerAvailabilities(playerAvailabilities)
    return jsonify({'message': 'PlayerAvailabilities added successfully!'}), 201