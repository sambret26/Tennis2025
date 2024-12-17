import stat
from models.PlayerBalance import PlayerBalance
from database import db

class PlayerBalanceRepository:

    @staticmethod
    def addPlayerBalance(playerBalance):
        db.session.add(playerBalance)
        db.session.commit()

    @staticmethod
    def addplayerBalances(playerBalances):
        db.session.addAll(playerBalances)
        db.session.commit()

    @staticmethod
    def getAllplayerBalances():
        return PlayerBalance.query.all()

    @staticmethod
    def getplayerBalanceById(playerBalanceId):
        return PlayerBalance.query.get(playerBalanceId)