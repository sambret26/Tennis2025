from flask import Blueprint, jsonify, request
from repositories.AvailabilityRepository import AvailabilityRepository
from models.Availability import Availability

availabilityBp = Blueprint('availabilityBp', __name__, url_prefix='/availabilities')

@availabilityBp.route('/', methods=['GET'])
def getAvailabilities():
    availabilities = AvailabilityRepository.getAllAvailabilities()
    return jsonify([availability.toDict() for availability in availabilities]), 200

@availabilityBp.route('/', methods=['POST'])
def addAvailability():
    availability = Availability.fromJson(request.json)
    AvailabilityRepository.addAvailability(availability)
    return jsonify({'message': 'Availability added successfully!'}), 201

@availabilityBp.route('/multiple', methods=['POST'])
def addAvailabilities():
    availabilities = []
    for data in request.json:
        availabilities.append(Availability.fromJson(data))
    AvailabilityRepository.addAvailabilities(availabilities)
    return jsonify({'message': 'Availabilities added successfully!'}), 201