from flask import Blueprint, jsonify, request
from repositories.CompetitionRepository import CompetitionRepository
from models.Competition import Competition

competitionRepository = CompetitionRepository()

competitionBp = Blueprint('competitionBp', __name__, url_prefix='/competitions')

@competitionBp.route('/', methods=['GET'])
def getCompetitions():
    competitions = competitionRepository.getAllCompetitions()
    return jsonify([competition.toDict() for competition in competitions]), 200

@competitionBp.route('/', methods=['POST'])
def addCompetition():
    competition = Competition.fromJson(request.json)
    competitionRepository.addCompetition(competition)
    return jsonify({'message': 'Competition added successfully!'}), 201
