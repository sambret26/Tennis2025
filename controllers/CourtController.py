from flask import Blueprint, jsonify, request
from repositories.CourtRepository import CourtRepository
from models.Court import Court

courtBp = Blueprint('courtBp', __name__, url_prefix='/courts')

@courtBp.route('/', methods=['GET'])
def getCourts():
    courts = CourtRepository.getAllCourts()
    return jsonify([court.toDict() for court in courts]), 200

@courtBp.route('/', methods=['POST'])
def addCourt():
    court = Court.fromJson(request.json)
    CourtRepository.addCourt(court)
    return jsonify({'message': 'Court added successfully!'}), 201

@courtBp.route('/multiple', methods=['POST'])
def addCourts():
    courts = []
    for data in request.json:
        courts.append(Court.fromJson(data))
    for court in courts:
        CourtRepository.addCourt(court)
    return jsonify({'message': 'Courts added successfully!'}), 201