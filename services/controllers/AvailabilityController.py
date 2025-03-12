from flask import Blueprint, jsonify
from repositories.AvailabilityRepository import AvailabilityRepository

availabilityRepository = AvailabilityRepository()

availabilityBp = Blueprint('availabilityBp', __name__, url_prefix='/availabilities')

@availabilityBp.route('/', methods=['GET'])
def getAvailabilities():
    availabilities = availabilityRepository.getAllAvailabilities()
    return jsonify([availability.toDict() for availability in availabilities]), 200