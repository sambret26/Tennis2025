from models.PlayerBalance import PlayerBalance
from database import db

class PlayerBalanceRepository:

    @staticmethod
    def addPlayerBalance(playerBalance):
        db.session.add(playerBalance)
        db.session.commit()

    @staticmethod
    def addplayerBalances(playerBalances):
        db.session.add_all(playerBalances)
        db.session.commit()

    @staticmethod
    def getAllplayerBalances():
        return PlayerBalance.query.all()

    @staticmethod
    def getplayerBalanceById(playerBalanceId):
        return PlayerBalance.query.get(playerBalanceId)

    @staticmethod
    def getPlayerBalanceByPlayerId(playerId):
        return PlayerBalance.query.filter_by(playerId=playerId).first()

    @staticmethod
    def updatePlayerBalanceForPlayerId(playerId, balance):
        PlayerBalance.query.filter_by(playerId=playerId).update({'remainingAmount': balance["remainingAmount"],
                                                                'finalAmount': balance["finalAmount"],
                                                                'initialAmount': balance["initialAmount"]})
        db.session.commit()

    @staticmethod
    def updatePlayerBalance(playerBalance):
        PlayerBalance.query.filter_by(id=playerBalance.id).update(playerBalance.toDict())
        db.session.commit()

    @staticmethod
    def deleteAllPlayerBalances():
        PlayerBalance.query.delete()
        db.session.commit()