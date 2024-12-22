from models.Team import Team
from database import db

class TeamRepository:

    @staticmethod
    def addTeam(team):
        db.session.add(team)
        db.session.commit()

    @staticmethod
    def addTeams(teams):
        db.session.addAll(teams)
        db.session.commit()

    @staticmethod
    def getAllTeams():
        return Team.query.all()

    @staticmethod
    def getTeamById(teamId):
        return Team.query.get(teamId)