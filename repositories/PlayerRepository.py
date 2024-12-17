from models.Player import Player
from database import db

class PlayerRepository:

    @staticmethod
    def getAllPlayers():
        return Player.query.all()

    @staticmethod
    def getPlayerById(id):
        return Player.query.get(id)

    @staticmethod
    def addPlayer(player):
        db.session.add(player)
        db.session.commit()

    @staticmethod
    def addPlayers(players):
        db.session.addAll(players)
        db.session.commit()

    @staticmethod
    def deletePlayer(player):
        db.session.delete(player)
        db.session.commit()
