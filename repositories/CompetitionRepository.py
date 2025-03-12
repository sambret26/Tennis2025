from models.Competition import Competition
from database import db

class CompetitionRepository:

    #GETTERS
    @staticmethod
    def getCompetitionById(competitionId):
        return Competition.query.get(competitionId)

    @staticmethod
    def getCompetitions():
        return Competition.query.order_by(Competition.label).all()

    @staticmethod
    def getDates():
        competition = Competition.query.filter_by(isActive=True).first()
        if competition is None:
            return None, None
        return competition.startDate, competition.endDate

    @staticmethod
    def getHomologationId():
        competition = Competition.query.filter(Competition.isActive is True).first()
        if competition is None:
            return None
        return competition.homologationId

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
    def updateCompetition(competitionId, competition):
        Competition.query.filter_by(id=competitionId).update(competition.toDictForDB())
        db.session.commit()

    @staticmethod
    def setActive(competitionId):
        Competition.query.filter_by(id=competitionId).update({Competition.isActive: 1})
        db.session.commit()

    @staticmethod
    def setInactive():
        Competition.query.filter_by(isActive=True).update({Competition.isActive: 0})
        db.session.commit()

    #DELETERS
    @staticmethod
    def deleteCompetition(competition):
        db.session.delete(competition)
        db.session.commit()

    @staticmethod
    def deleteCompetitions(competitionsId):
        Competition.query.filter(Competition.homologationId.in_(competitionsId)).delete()
        db.session.commit()