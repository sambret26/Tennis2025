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

    @staticmethod
    def getTeamByPlayersIds(player1Id, player2Id):
        return Team.query.filter_by(player1Id=player1Id, player2Id=player2Id).first()

    @staticmethod
    def getAllTeamsId():
        return [team.id for team in Team.query.all()]

    @staticmethod
    def getTeamsMap():
        return {team.fftId: team for team in Team.query.all()}

    #ADDERS
    @staticmethod
    def addTeam(team):
        db.session.add(team)
        db.session.commit()

    @staticmethod
    def addTeams(teams):
        db.session.add_all(teams)
        db.session.commit()

    #DELETERS
    @staticmethod
    def deleteTeams(teamsId):
        Team.query.filter(Team.id.in_(teamsId)).delete()
        db.session.commit()

    @staticmethod
    def deleteAllTeams():
        Team.query.delete()
        db.session.commit()