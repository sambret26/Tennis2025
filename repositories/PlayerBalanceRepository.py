from models.PlayerBalance import PlayerBalance
from database import db

class PlayerBalanceRepository:

    @staticmethod
    def addplayerBalance(playerBalance):
        db.session.add(playerBalance)
        db.session.commit()

    @staticmethod
    def getAllplayerBalances():
        return PlayerBalance.query.all()

    @staticmethod
    def getplayerBalanceById(playerBalanceId):
        return PlayerBalance.query.get(playerBalanceId)