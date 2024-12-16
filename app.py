from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Configuration de la base de données (sera remplacée par une URL PostgreSQL sur Railway)
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle pour la table Player
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

# Repository pour requêter la base
class PlayerRepository:
    @staticmethod
    def get_all_players():
        return Player.query.all()

    @staticmethod
    def add_player(first_name, last_name):
        new_player = Player(first_name=first_name, last_name=last_name)
        db.session.add(new_player)
        db.session.commit()

# Route GET : Récupérer tous les joueurs
@app.route('/players', methods=['GET'])
def get_players():
    players = PlayerRepository.get_all_players()
    return jsonify([
        {"id": player.id, "first_name": player.first_name, "last_name": player.last_name}
        for player in players
    ])

# Initialisation de la base de données pour la première fois
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas encore
    app.run(debug=True)