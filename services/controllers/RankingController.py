from flask import Blueprint, jsonify, request
from repositories.RankingRepository import RankingRepository
from models.Ranking import Ranking

rankingRepository = RankingRepository()
rankingBp = Blueprint('rankingBp', __name__, url_prefix='/rankings')

@rankingBp.route('/', methods=['GET'])
def getRankings():
    rankings = rankingRepository.getAllRankings()
    return jsonify([ranking.toDict() for ranking in rankings]), 200

@rankingBp.route('/', methods=['POST'])
def addRanking():
    ranking = Ranking.fromJson(request.json)
    rankingRepository.addRanking(ranking)
    return jsonify({'message': 'Ranking added successfully!'}), 201
