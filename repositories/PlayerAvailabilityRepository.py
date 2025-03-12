from models.PlayerAvailability import PlayerAvailability
from database import db

class PlayerAvailabilityRepository:

    #GETTERS
    @staticmethod
    def getAllPlayerAvailabilities():
        return PlayerAvailability.query.all()

    @staticmethod
    def getPlayerAvailabilityByDay(day):
        return PlayerAvailability.query.filter_by(day=day).all()

    @staticmethod
    def getPlayerAvailabilityIdByPlayerIdDayTimeSlot(playerId, day, timeSlot):
        return PlayerAvailability.query.with_entities(PlayerAvailability.id)\
            .filter_by(playerId=playerId, day=day, timeSlot=timeSlot).first()

    @staticmethod
    def getPlayerAvailabilityByPlayerId(playerId):
        return PlayerAvailability.query.filter_by(playerId=playerId).all()

    #ADDERS
    @staticmethod
    def addPlayerAvailability(playerAvailability):
        db.session.add(playerAvailability)
        db.session.commit()

    @staticmethod
    def addPlayerAvailabilities(playerAvailabilities):
        db.session.add_all(playerAvailabilities)
        db.session.commit()

    #SETTERS
    @staticmethod
    def updatePlayerAvailability(playerAvailabilityId, available):
        PlayerAvailability.query.filter_by(id=playerAvailabilityId).update({"available": available})
        db.session.commit()

    #DELETERS
    @staticmethod
    def deleteAllPlayerAvailabilities():
        PlayerAvailability.query.delete()
        db.session.commit()