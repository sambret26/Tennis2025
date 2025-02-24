from models.Team import Team
from database import db

class TeamRepository:

    #GETTERS
    @staticmethod
    def getAllTeams():
        return Team.query.all()

    @staticmethod
    def getTeamByFftId(fftId):
        return Team.query.filter_by(fftId=fftId).first()

    @staticmethod
    def getTeamById(teamId):
        return Team.query.get(teamId)

    #ADDERS
    @staticmethod
    def addTeam(team):
        db.session.add(team)
        db.session.commit()

    @staticmethod
    def addTeams(teams):
        db.session.add_all(teams)
        db.session.commit()

    #SETTERS
    @staticmethod
    def setTeamsToActive(teamsId):
        Team.query.filter(Team.id.in_(teamsId)).update({'isActive': True})
        db.session.commit()

    @staticmethod
    def setTeamsToInactive():
        Team.query.update({'isActive': False})
        db.session.commit()

    #DELETERS
    @staticmethod
    def deleteInactiveTeams():
        Team.query.filter_by(isActive=False).delete()
        db.session.commit()