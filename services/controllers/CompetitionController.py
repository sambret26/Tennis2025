from flask import Blueprint, jsonify, request
from repositories.CompetitionRepository import CompetitionRepository
from services.business import CompetitionBusiness
from models.Competition import Competition

competitionRepository = CompetitionRepository()

competitionBp = Blueprint('competitionBp', __name__, url_prefix='/competitions')

@competitionBp.route('/', methods=['GET'])
def getCompetitions():
    competitions = competitionRepository.getCompetitions()
    return jsonify([competition.toDict() for competition in competitions]), 200

@competitionBp.route('/', methods=['POST'])
def addCompetition():
    competition = Competition.fromJson(request.json)
    competitionRepository.addCompetition(competition)
    return jsonify({'message': 'Competition added successfully!'}), 201

@competitionBp.route('/', methods=['PUT'])
def updateCompetition():
    competition = Competition.fromJson(request.json)
    competitionRepository.updateCompetition(competition)
    return jsonify({'message': 'Competition updated successfully!'}), 200

@competitionBp.route('/', methods=['DELETE'])
def deleteCompetition():
    competition = Competition.fromJson(request.json)
    competitionRepository.deleteCompetition(competition)
    return jsonify({'message': 'Competition deleted successfully!'}), 200

@competitionBp.route('/update', methods=['POST'])
def updateCompetitions():
    result = CompetitionBusiness.updateCompetitions()
    if result == None:
        return jsonify({'message': 'No competitions found!'}), 404
    return jsonify({'message': 'Competitions updated successfully!'}), 200

@competitionBp.route('/dates', methods=['GET'])
def getDates():
    dates =  competitionRepository.getDates()
    if dates == (None, None):
        return jsonify({'message': 'No competitions found!'}), 404
    return jsonify({'startDate': dates[0], 'endDate': dates[1]}), 200

@competitionBp.route('/active', methods=['PUT'])
def activeCompetition():
    competitionId = request.json['competitionId']
    competitionRepository.setInactive()
    competitionRepository.setActive(competitionId)
    return jsonify({'message': 'Competition updated successfully!'}), 200