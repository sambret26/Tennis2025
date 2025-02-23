from flask import Blueprint, jsonify, request
from repositories.AvailabilityRepository import AvailabilityRepository
from models.Availability import Availability

availabilityRepository = AvailabilityRepository()

availabilityBp = Blueprint('availabilityBp', __name__, url_prefix='/availabilities')

@availabilityBp.route('/', methods=['GET'])
def getAvailabilities():
    availabilities = availabilityRepository.getAllAvailabilities()
    return jsonify([availability.toDict() for availability in availabilities]), 200

@availabilityBp.route('/', methods=['POST'])
def addAvailability():
    availability = Availability.fromJson(request.json)
    availabilityRepository.addAvailability(availability)
    return jsonify({'message': 'Availability added successfully!'}), 201