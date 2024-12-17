from flask import Flask
from config import Config
from database import db
from controllers.PlayerController import playerBp
from controllers.AvailabilityController import availabilityBp
from controllers.CategoryController import categoryBp
from controllers.CourtController import courtBp
from controllers.MatchController import matchBp
from controllers.PlayerBalanceController import playerBalanceBp
from controllers.PlayerCategoriesController import playerCategoriesBp
from controllers.RankingController import rankingBp
from controllers.ReductionController import reductionBp
from controllers.ReductionSettingsController import reductionSettingsBp
from controllers.SettingController import settingBp
from controllers.TeamController import teamBp
from controllers.TransactionController import transactionBp

from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

CORS(app)

# Registering blueprints
app.register_blueprint(playerBp)
app.register_blueprint(availabilityBp)
app.register_blueprint(categoryBp)
app.register_blueprint(courtBp)
app.register_blueprint(matchBp)
app.register_blueprint(playerBalanceBp)
app.register_blueprint(playerCategoriesBp)
app.register_blueprint(rankingBp)
app.register_blueprint(reductionBp)
app.register_blueprint(reductionSettingsBp)
app.register_blueprint(settingBp)
app.register_blueprint(teamBp)
app.register_blueprint(transactionBp)

# Création des tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)