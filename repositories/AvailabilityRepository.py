from models.Availability import Availability
from database import db

class AvailabilityRepository:

    #GETTERS
    @staticmethod
    def getAllAvailabilities():
        return Availability.query.order_by(Availability.number).all()