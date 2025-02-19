from models.PlayerAvailabilityComment import PlayerAvailabilityComment
from database import db

class PlayerAvailabilityCommentRepository:

    @staticmethod
    def addPlayerAvailabilityComment(comment):
        db.session.add(comment)
        db.session.commit()

    @staticmethod
    def getPlayerAvailabilityComment(playerId, day):
        return PlayerAvailabilityComment.query.filter_by(playerId=playerId, day=day).first()

    @staticmethod
    def getAllCommentsForDay(day):
        return PlayerAvailabilityComment.query.filter_by(day=day).all()

    @staticmethod
    def updatePlayerAvailabilityComment(comment, comments):
        comment.comments = comments
        db.session.commit()

    @staticmethod
    def deletePlayerAvailabilityComment(playerId, day):
        PlayerAvailabilityComment.query.filter_by(playerId=playerId, day=day).delete()
        db.session.commit()

    @staticmethod
    def deleteAllPlayerAvailabilityComments():
        PlayerAvailabilityComment.query.delete()
        db.session.commit()