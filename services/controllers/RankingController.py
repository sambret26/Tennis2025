from flask import Blueprint
from repositories.RankingRepository import RankingRepository

rankingRepository = RankingRepository()
rankingBp = Blueprint('rankingBp', __name__, url_prefix='/rankings')