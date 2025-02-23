from flask import Blueprint, jsonify, request
from repositories.PlayerAvailabilityRepository import PlayerAvailabilityRepository
from models.PlayerAvailability import PlayerAvailability

playerAvailabilityRepository = PlayerAvailabilityRepository()

playerAvailabilityBp = Blueprint('playerAvailabilityBp', __name__, url_prefix='/playerAvailabilities')

@playerAvailabilityBp.route('/all', methods=['GET'])
def getPlayerAvailabilities():
    playerAvailabilities = playerAvailabilityRepository.getAllPlayerAvailabilities()
    return jsonify([playerAvailability.toDict() for playerAvailability in playerAvailabilities]), 200

@playerAvailabilityBp.route('/player/<int:playerId>', methods=['GET'])
def getPlayerAvailabilitiesByPlayerId(playerId):
    playerAvailabilities = playerAvailabilityRepository.getPlayerAvailabilityByPlayerId(playerId)
    return jsonify([playerAvailability.toDict() for playerAvailability in playerAvailabilities]), 200

@playerAvailabilityBp.route('/date', methods=['GET'])
def getAvailabilitiesForDay():
    date = request.args.get('date')
    playerAvailabilities = playerAvailabilityRepository.getPlayerAvailabilityByDay(date)
    return jsonify([playerAvailability.toDict() for playerAvailability in playerAvailabilities]), 200

@playerAvailabilityBp.route('/', methods=['POST'])
def addPlayerAvailability():
    playerAvailability = PlayerAvailability.fromJson(request.json)
    playerAvailabilityRepository.addPlayerAvailability(playerAvailability)
    return jsonify({'message': 'PlayerAvailability added successfully!'}), 201

@playerAvailabilityBp.route('/update', methods=['POST'])
def updatePlayerAvailability():
    playerAvailability = PlayerAvailability.fromJson(request.json)
    result = playerAvailabilityRepository.getPlayerAvailabilityIdByPlayerIdDayTimeSlot(playerAvailability.playerId, playerAvailability.day, playerAvailability.timeSlot)
    id = result[0] if result else None
    if id:
        playerAvailabilityRepository.updatePlayerAvailability(id, playerAvailability.available)
        return jsonify({'message': 'PlayerAvailability created successfully!'}), 200
    playerAvailabilityRepository.addPlayerAvailability(playerAvailability)
    return jsonify({'message': 'PlayerAvailability updated successfully!'}), 200
