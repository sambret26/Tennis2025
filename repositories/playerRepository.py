from models.player import Player
from database import db

class PlayerRepository:

    @staticmethod
    def get_all_players():
        return Player.query.all()

    @staticmethod
    def get_player_by_id(id):
        return Player.query.get(id)

    @staticmethod
    def add_player(player):
        db.session.add(player)
        db.session.commit()

    @staticmethod
    def delete_player(player):
        db.session.delete(player)
        db.session.commit()