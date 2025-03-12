from flask import Blueprint, jsonify, request
from repositories.MatchRepository import MatchRepository

matchRepository = MatchRepository()

matchBp = Blueprint('matchBp', __name__, url_prefix='/matches')

@matchBp.route('/planning', methods=['GET'])
def getMatchesForPlanning():
    date = request.args.get('date')
    matches = matchRepository.getMatchesForPlanning(date)
    return jsonify([match.toDict() for match in matches]), 200

@matchBp.route('/result', methods=['POST'])
def updateMatchResult():
    data = request.json
    matchId = data['matchId']
    winnerId = data['playerId']
    score = data['score']
    finish = data['finish']
    double = data['double']
    match = matchRepository.getMatchById(matchId)
    if not match:
        return jsonify({'message': 'Match not found!'}), 404
    if double :
        match.teamWinnerId = winnerId
    else :
        match.winnerId = winnerId
    match.score = score
    match.finish = finish
    matchRepository.updateMatch(match)
    return jsonify({'message': 'Match result updated successfully!'}), 200

@matchBp.route('/playerAvailability', methods=['POST'])
def updateMatchAvailability():
    data = request.json
    matchId = data['matchId']
    playerNumber = data['playerNumber']
    available = data['available']
    match = matchRepository.getMatchById(matchId)
    if not match:
        return jsonify({'message': 'Match not found!'}), 404
    if playerNumber == 1:
        match.player1Availability = available
    elif playerNumber == 2:
        match.player2Availability = available
    matchRepository.updateMatch(match)
    return jsonify({'message': 'Match availability updated successfully!'}), 200