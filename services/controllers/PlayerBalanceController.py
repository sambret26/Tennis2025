from flask import Blueprint
from repositories.PlayerBalanceRepository import PlayerBalanceRepository

playerBalanceRepository = PlayerBalanceRepository()

playerBalanceBp = Blueprint('playerBalanceBp', __name__, url_prefix='/playerBalances')