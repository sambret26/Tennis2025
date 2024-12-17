from flask import Flask
from config import Config
from database import db
from controllers.PlayerController import playerBp
from controllers.AvailabilityController import availability_bp
from controllers.CategoryController import category_bp
from controllers.CourtController import court_bp
from controllers.MatchController import match_bp
from controllers.PlayerBalanceController import player_balance_bp
from controllers.PlayerCategoriesController import player_categories_bp
from controllers.RankingController import ranking_bp
from controllers.ReductionController import reduction_bp
from controllers.ReductionSettingsController import reduction_settings_bp
from controllers.SettingController import setting_bp
from controllers.TeamController import team_bp
from controllers.TransactionController import transaction_bp

from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

CORS(app)

# Registering blueprints
app.register_blueprint(playerBp)
app.register_blueprint(availability_bp)
app.register_blueprint(category_bp)
app.register_blueprint(court_bp)
app.register_blueprint(match_bp)
app.register_blueprint(player_balance_bp)
app.register_blueprint(player_categories_bp)
app.register_blueprint(ranking_bp)
app.register_blueprint(reduction_bp)
app.register_blueprint(reduction_settings_bp)
app.register_blueprint(setting_bp)
app.register_blueprint(team_bp)
app.register_blueprint(transaction_bp)

# Création des tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)