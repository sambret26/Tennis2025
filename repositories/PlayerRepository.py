from models.Player import Player
from models.PlayerCategories import PlayerCategories
from database import db

class PlayerRepository:

    @staticmethod
    def getAllPlayers():
        return Player.query.all()

    @staticmethod
    def getAllPlayerNames():
        results = Player.query.with_entities(Player.id, Player.firstName, Player.lastName).all()
        players = [Player(id=result[0], firstName=result[1], lastName=result[2]) for result in results]
        return players

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

    @staticmethod
    def getNumberPlayers():
        return Player.query.count()

    @staticmethod
    def getRankingIds():
        results = Player.query.with_entities(Player.rankingId).all()
        return [result[0] for result in results]

    @staticmethod
    def getRankingIdsByCategoryId(categoryId):
        results = db.session.query(Player.rankingId).select_from(Player).join(PlayerCategories, Player.id == PlayerCategories.playerId).filter(PlayerCategories.categoryId == categoryId).all()
        return [result[0] for result in results]
