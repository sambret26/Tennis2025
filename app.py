from flask import Flask
from config import Config
from database import db
from controllers.playerController import player_bp


from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

db.init_app(app)
app.register_blueprint(player_bp)

# Création des tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)