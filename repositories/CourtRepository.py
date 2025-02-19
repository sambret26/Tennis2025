from models.Court import Court
from database import db

class CourtRepository:

    @staticmethod
    def addCourt(court):
        db.session.add(court)
        db.session.commit()

    @staticmethod
    def addCourts(courts):
        db.session.add_all(courts)
        db.session.commit()

    @staticmethod
    def getAllCourts():
        return Court.query.all()

    @staticmethod
    def getCourtById(courtId):
        return Court.query.get(courtId)

    @staticmethod
    def deleteAllCourts():
        Court.query.delete()
        db.session.commit()