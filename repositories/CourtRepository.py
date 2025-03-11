from models.Court import Court
from database import db

class CourtRepository:

    #GETTERS
    @staticmethod
    def getAllCourts():
        return Court.query.all()

    @staticmethod
    def getCourtById(courtId):
        return Court.query.get(courtId)

    @staticmethod
    def getCourtsMap():
        return {court.fftId: court.id for court in Court.query.all()}

    #ADDERS
    @staticmethod
    def addCourt(court):
        db.session.add(court)
        db.session.commit()

    @staticmethod
    def addCourts(courts):
        db.session.add_all(courts)
        db.session.commit()

    #DELETERS
    @staticmethod
    def deleteAllCourts():
        Court.query.delete()
        db.session.commit()