from flask import Blueprint, jsonify, request
from models.PlayerAvailabilityComment import PlayerAvailabilityComment
from repositories.PlayerAvailabilityCommentRepository import PlayerAvailabilityCommentRepository

playerAvailabilityCommentRepository = PlayerAvailabilityCommentRepository()

playerAvailabilityCommentBp = Blueprint('playerAvailabilityComment', __name__, url_prefix='/playerAvailabilityComment')

@playerAvailabilityCommentBp.route('/', methods=['POST'])
def createOrUpdateComment():
    comment = PlayerAvailabilityComment.fromJson(request.json)
    commentInDB = playerAvailabilityCommentRepository.getPlayerAvailabilityComment(comment.playerId, comment.day)
    if commentInDB:
        playerAvailabilityCommentRepository.updatePlayerAvailabilityComment(commentInDB, comment.comments)
    else:
        playerAvailabilityCommentRepository.addPlayerAvailabilityComment(comment)
    return jsonify({'message': 'Comment saved successfully'})

@playerAvailabilityCommentBp.route('/<string:day>', methods=['GET'])
def getAllCommentsForDay(day):
    comments = playerAvailabilityCommentRepository.getAllCommentsForDay(day)
    return jsonify([comment.toDict() for comment in comments])