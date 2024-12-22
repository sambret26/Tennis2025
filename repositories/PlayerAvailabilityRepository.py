from models.PlayerAvailability import PlayerAvailability
from database import db

class PlayerAvailabilityRepository:

    @staticmethod
    def addPlayerAvailability(playerAvailability):
        db.session.add(playerAvailability)
        db.session.commit()

    @staticmethod
    def addPlayerAvailabilities(playerAvailabilities):
        db.session.addAll(playerAvailabilities)
        db.session.commit()

    @staticmethod
    def updatePlayerAvailability(id, available):
        PlayerAvailability.query.filter_by(id=id).update({"available": available})
        db.session.commit()

    @staticmethod
    def getAllPlayerAvailabilities():
        return PlayerAvailability.query.all()

    @staticmethod
    def getPlayerAvailabilityIdByPlayerIdDayTimeSlot(playerId, day, timeSlot):
        return PlayerAvailability.query.with_entities(PlayerAvailability.id).filter_by(playerId=playerId, day=day, timeSlot=timeSlot).first()

    @staticmethod
    def getPlayerAvailabilityByPlayerId(playerId):
        return PlayerAvailability.query.filter_by(playerId=playerId).all()