from models.Availability import Availability
from database import db

class AvailabilityRepository:

    #GETTERS
    @staticmethod
    def getAllAvailabilities():
        return Availability.query.order_by(Availability.number).all()

    #ADDERS
    @staticmethod
    def addAvailability(availability):
        db.session.add(availability)
        db.session.commit()