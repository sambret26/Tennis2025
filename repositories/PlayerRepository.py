from models.Player import Player
from models.PlayerCategories import PlayerCategories
from database import db

class PlayerRepository:

    #GETTERS
    @staticmethod
    def getAllPlayers():
        return Player.query.all()

    @staticmethod
    def getAllPlayerNames():
        results = Player.query.with_entities(Player.id, Player.firstName, Player.lastName).all()
        players = [Player(id=r[0], firstName=r[1], lastName=r[2]) for r in results]
        return players

    @staticmethod
    def getPlayerById(playerId):
        return Player.query.get(playerId)

    @staticmethod
    def getPlayerByFftId(fftId):
        return Player.query.filter_by(fftId=fftId).first()

    @staticmethod
    def getNumberPlayers():
        return Player.query.count()

    @staticmethod
    def getRankingIds():
        results = Player.query.with_entities(Player.rankingId).all()
        return [result[0] for result in results]

    @staticmethod
    def getRankingIdsByCategoryId(categoryId):
        results = db.session.query(Player.rankingId).select_from(Player)\
            .join(PlayerCategories, Player.id == PlayerCategories.playerId)\
            .filter(PlayerCategories.categoryId == categoryId).all()
        return [result[0] for result in results]

    @staticmethod
    def getPlayersIdMap():
        return {player.fftId: player.id for player in Player.query.all()}

    @staticmethod
    def getPlayersMap():
        return {player.fftId: player for player in Player.query.all()}

    #ADDERS
    @staticmethod
    def addPlayer(player):
        db.session.add(player)
        db.session.commit()
        return player

    @staticmethod
    def addPlayers(players):
        db.session.add_all(players)
        db.session.commit()

    #SETTERS
    @staticmethod
    def updatePlayer(playerId, player):
        Player.query.filter_by(id=playerId).update(player.toDictForDB())
        db.session.commit()

    #DELETERS
    @staticmethod
    def deletePlayerById(playerId):
        Player.query.filter_by(id=playerId).delete()
        db.session.commit()

    @staticmethod
    def deletePlayer(player):
        db.session.delete(player)
        db.session.commit()

    @staticmethod
    def deletePlayers(playersIds):
        Player.query.filter(Player.id.in_(playersIds)).delete()
        db.session.commit()

    @staticmethod
    def deleteAllPlayers():
        Player.query.delete()
        db.session.commit()