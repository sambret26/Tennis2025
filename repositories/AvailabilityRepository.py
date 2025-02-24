from models.Availability import Availability
from database import db

class AvailabilityRepository:

    #GETTERS
    @staticmethod
    def getAllAvailabilities():
        return Availability.query.order_by(Availability.number).all()

    @staticmethod
    def getAvailabilityById(availabilityId):
        return Availability.query.get(availabilityId)

    #ADDERS
    @staticmethod
    def addAvailability(availability):
        db.session.add(availability)
        db.session.commit()

    @staticmethod
    def addAvailabilities(availabilities):
        db.session.add_all(availabilities)
        db.session.commit()

