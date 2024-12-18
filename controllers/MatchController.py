from flask import Blueprint, jsonify, request
from repositories.MatchRepository import MatchRepository
from models.Match import Match

matchBp = Blueprint('matchBp', __name__, url_prefix='/matches')

@matchBp.route('/', methods=['GET'])
def getMatch():
    matches = MatchRepository.getAllMatch()
    return jsonify([match.toDict() for match in matches]), 200

@matchBp.route('/planning', methods=['GET'])
def getMatchesForPlanning():
    date = request.args.get('date')
    matches = MatchRepository.getMatchesForPlanning(date)
    return jsonify([match.toDict() for match in matches]), 200

@matchBp.route('/', methods=['POST'])
def addMatch():
    match = Match.fromJson(request.json)
    MatchRepository.addMatch(match)
    return jsonify({'message': 'Match added successfully!'}), 201

@matchBp.route('/multiple', methods=['POST'])
def addMatches():
    matches = []
    for data in request.json:
        matches.append(Match.fromJson(data))
    MatchRepository.addMatches(matches)
    return jsonify({'message': 'Matches added successfully!'}), 201

@matchBp.route('/result', methods=['POST'])
def updateMatchResult():
    data = request.json
    matchId = data['matchId']
    winnerId = data['playerId']
    score = data['score']
    match = MatchRepository.getMatchById(matchId)
    if not match:
        return jsonify({'message': 'Match not found!'}), 404
    match.winnerId = winnerId
    match.score = score
    MatchRepository.updateMatch(match)
    return jsonify({'message': 'Match result updated successfully!'}), 200