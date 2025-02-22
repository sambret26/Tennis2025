from flask import Blueprint, jsonify, request
from repositories.TeamRepository import TeamRepository
from models.Team import Team

teamRepository = TeamRepository()

teamBp = Blueprint('teamBp', __name__, url_prefix='/teams')

@teamBp.route('/', methods=['GET'])
def getTeams():
    teams = teamRepository.getAllTeams()
    return jsonify([team.toDict() for team in teams]), 200

@teamBp.route('/', methods=['POST'])
def addTeam():
    team = Team.fromJson(request.json)
    teamRepository.addTeam(team)
    return jsonify({'message': 'Team added successfully!'}), 201
