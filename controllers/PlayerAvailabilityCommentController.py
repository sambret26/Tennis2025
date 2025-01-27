from flask import Blueprint, jsonify, request
from models.PlayerAvailabilityComment import PlayerAvailabilityComment
from database import db

playerAvailabilityCommentBp = Blueprint('playerAvailabilityComment', __name__)

@playerAvailabilityCommentBp.route('/player-availability-comment/<int:playerId>/<string:day>', methods=['GET'])
def get_player_comment(playerId, day):
    """Récupère le commentaire d'un joueur pour un jour donné"""
    comment = PlayerAvailabilityComment.query.filter_by(
        playerId=playerId,
        day=day
    ).first()
    
    if comment:
        return jsonify(comment.toDict())
    return jsonify(None)

@playerAvailabilityCommentBp.route('/player-availability-comment', methods=['POST'])
def create_or_update_comment():
    """Crée ou met à jour le commentaire d'un joueur pour un jour donné"""
    data = request.json
    
    comment = PlayerAvailabilityComment.query.filter_by(
        playerId=data['playerId'],
        day=data['day']
    ).first()
    
    if comment:
        comment.comments = data.get('comments')
    else:
        comment = PlayerAvailabilityComment.fromJson(data)
        db.session.add(comment)
    
    try:
        db.session.commit()
        return jsonify(comment.toDict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@playerAvailabilityCommentBp.route('/player-availability-comments/<string:day>', methods=['GET'])
def get_all_comments_for_day(day):
    """Récupère tous les commentaires pour un jour donné"""
    comments = PlayerAvailabilityComment.query.filter_by(day=day).all()
    return jsonify([comment.toDict() for comment in comments])

@playerAvailabilityCommentBp.route('/player-availability-comment/<int:playerId>/<string:day>', methods=['DELETE'])
def delete_comment(playerId, day):
    """Supprime le commentaire d'un joueur pour un jour donné"""
    comment = PlayerAvailabilityComment.query.filter_by(
        playerId=playerId,
        day=day
    ).first()
    
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404
    
    try:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comment deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
