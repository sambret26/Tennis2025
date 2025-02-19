from flask import Blueprint, jsonify, request
from models.PlayerAvailabilityComment import PlayerAvailabilityComment
from repositories.PlayerAvailabilityCommentRepository import PlayerAvailabilityCommentRepository

playerAvailabilityCommentRepository = PlayerAvailabilityCommentRepository()

playerAvailabilityCommentBp = Blueprint('playerAvailabilityComment', __name__)

@playerAvailabilityCommentBp.route('/player-availability-comment/<int:playerId>/<string:day>', methods=['GET'])
def getPlayerComment(playerId, day):
    comment = playerAvailabilityCommentRepository.getPlayerAvailabilityComment(playerId, day)
    if comment:
        return jsonify(comment.toDict())
    return jsonify(None)

@playerAvailabilityCommentBp.route('/player-availability-comment', methods=['POST'])
def createOrUpdateComment():
    comment = PlayerAvailabilityComment.fromJson(request.json)

    commentInDB = playerAvailabilityCommentRepository.getPlayerAvailabilityComment(comment.playerId, comment.day)
    
    if commentInDB:
        playerAvailabilityCommentRepository.updatePlayerAvailabilityComment(commentInDB, comment.comments)
    else:
        playerAvailabilityCommentRepository.addPlayerAvailabilityComment(comment)

@playerAvailabilityCommentBp.route('/player-availability-comments/<string:day>', methods=['GET'])
def getAllCommentsForDay(day):
    comments = playerAvailabilityCommentRepository.getAllCommentsForDay(day)
    return jsonify([comment.toDict() for comment in comments])

@playerAvailabilityCommentBp.route('/player-availability-comment/<int:playerId>/<string:day>', methods=['DELETE'])
def deleteComment(playerId, day):
    playerAvailabilityCommentRepository.deletePlayerAvailabilityComment(playerId, day)
    return jsonify({'message': 'Comment deleted successfully'})