from models.Competition import Competition
from database import db

class CompetitionRepository:

    #GETTERS
    @staticmethod
    def getCompetitionById(competitionId):
        return Competition.query.get(competitionId)

    @staticmethod
    def getActiveCompetition():
        return Competition.query.filter_by(isActive=True).first()

    @staticmethod
    def getAllCompetitions():
        return Competition.query.order_by(Competition.label).all()

    #ADDERS
    @staticmethod
    def addCompetition(competition):
        db.session.add(competition)
        db.session.commit()

    @staticmethod
    def addCompetitions(competitions):
        db.session.add_all(competitions)
        db.session.commit()

    #SETTERS
    @staticmethod
    def inactiveCompetition():
        Competition.query.filter_by(isActive=True).update({'isActive': False})
        db.session.commit()

    @staticmethod
    def activeCompetition(competitionId):
        Competition.query.filter_by(id=competitionId).update({'isActive': True})
        db.session.commit()