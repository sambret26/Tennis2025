from flask import Blueprint, jsonify, request
from repositories.RankingRepository import RankingRepository
from models.Ranking import Ranking

rankingBp = Blueprint('rankingBp', __name__, url_prefix='/rankings')

@rankingBp.route('/', methods=['GET'])
def getRankings():
    rankings = RankingRepository.getAllRankings()
    return jsonify([ranking.toDict() for ranking in rankings]), 200

@rankingBp.route('/', methods=['POST'])
def addRanking():
    ranking = Ranking.fromJson(request.json)
    RankingRepository.addRanking(ranking)
    return jsonify({'message': 'Ranking added successfully!'}), 201

@rankingBp.route('/multiple', methods=['POST'])
def addRankings():
    rankings = []
    for data in request.json:
        rankings.append(Ranking.fromJson(data))
    RankingRepository.addRankings(rankings)
    return jsonify({'message': 'Rankings added successfully!'}), 201