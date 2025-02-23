from flask import Blueprint, jsonify, request
from repositories.CourtRepository import CourtRepository
from models.Court import Court

courtRepository = CourtRepository()

courtBp = Blueprint('courtBp', __name__, url_prefix='/courts')

@courtBp.route('/', methods=['GET'])
def getCourts():
    courts = courtRepository.getAllCourts()
    return jsonify([court.toDict() for court in courts]), 200

@courtBp.route('/', methods=['POST'])
def addCourt():
    court = Court.fromJson(request.json)
    courtRepository.addCourt(court)
    return jsonify({'message': 'Court added successfully!'}), 201
