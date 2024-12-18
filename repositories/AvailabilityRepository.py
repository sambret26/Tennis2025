from models.Availability import Availability
from database import db

class AvailabilityRepository:

    @staticmethod
    def addAvailability(availability):
        db.session.add(availability)
        db.session.commit()

    @staticmethod
    def addAvailabilities(availabilities):
        db.session.addAll(availabilities)
        db.session.commit()

    @staticmethod
    def getAllAvailabilities():
        return Availability.query.all()

    @staticmethod
    def getAvailabilityById(availabilityId):
        return Availability.query.get(availabilityId)