from flask import Blueprint, jsonify, request
from repositories.PlayerAvailabilityRepository import PlayerAvailabilityRepository
from models.PlayerAvailability import PlayerAvailability

playerAvailabilityRepository = PlayerAvailabilityRepository()

playerAvailabilityBp = Blueprint('playerAvailabilityBp', __name__, url_prefix='/playerAvailabilities')

@playerAvailabilityBp.route('/all', methods=['GET'])
def getPlayerAvailabilities():
    playerAvailabilities = playerAvailabilityRepository.getAllPlayerAvailabilities()
    return jsonify([playerAvailability.toDict() for playerAvailability in playerAvailabilities]), 200

@playerAvailabilityBp.route('/date', methods=['GET'])
def getAvailabilitiesForDay():
    date = request.args.get('date')
    playerAvailabilities = playerAvailabilityRepository.getPlayerAvailabilityByDay(date)
    return jsonify([playerAvailability.toDict() for playerAvailability in playerAvailabilities]), 200

@playerAvailabilityBp.route('/update', methods=['POST'])
def updatePlayerAvailability():
    pa = PlayerAvailability.fromJson(request.json)
    result = playerAvailabilityRepository.getPlayerAvailabilityIdByPlayerIdDayTimeSlot(pa.playerId, pa.day, pa.timeSlot)
    paId = result[0] if result else None
    if paId:
        playerAvailabilityRepository.updatePlayerAvailability(paId, pa.available)
        return jsonify({'message': 'PlayerAvailability updated successfully!'}), 200
    playerAvailabilityRepository.addPlayerAvailability(pa)
    return jsonify({'message': 'PlayerAvailability created successfully!'}), 200
