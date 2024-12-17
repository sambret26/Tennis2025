from flask import Blueprint, jsonify, request
from repositories.TeamRepository import TeamRepository
from models.Team import Team

teamBp = Blueprint('teamBp', __name__, url_prefix='/teams')

@teamBp.route('/', methods=['GET'])
def getTeams():
    teams = TeamRepository.getAllTeams()
    return jsonify([team.toDict() for team in teams]), 200

@teamBp.route('/', methods=['POST'])
def addTeam():
    team = Team.fromJson(request.json)
    TeamRepository.addTeam(team)
    return jsonify({'message': 'Team added successfully!'}), 201

@teamBp.route('/multiple', methods=['POST'])
def addTeams():
    teams = []
    for data in request.json:
        teams.append(Team.fromJson(data))
    for team in teams:
        TeamRepository.addTeam(team)
    return jsonify({'message': 'Teams added successfully!'}), 201