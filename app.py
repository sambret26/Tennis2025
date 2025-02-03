from flask import Flask
from config import Config
from database import db
from services.controllers.PlayerController import playerBp
from services.controllers.AccountController import accountBp
from services.controllers.AvailabilityController import availabilityBp
from services.controllers.CategoryController import categoryBp
from services.controllers.CourtController import courtBp
from services.controllers.MatchController import matchBp
from services.controllers.PlayerAvailabilityController import playerAvailabilityBp
from services.controllers.PlayerBalanceController import playerBalanceBp
from services.controllers.PlayerCategoriesController import playerCategoriesBp
from services.controllers.RankingController import rankingBp
from services.controllers.ReductionController import reductionBp
from services.controllers.ReductionSettingsController import reductionSettingsBp
from services.controllers.SettingController import settingBp
from services.controllers.TeamController import teamBp
from services.controllers.TransactionController import transactionBp
from services.controllers.PlayerAvailabilityCommentController import playerAvailabilityCommentBp
from services.controllers.PaymentController import paymentBp
from services.controllers.ProfilController import profilBp
from services.controllers.UserController import userBp

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
db.init_app(app)


# Registering blueprints
app.register_blueprint(playerBp)
app.register_blueprint(playerAvailabilityBp)
app.register_blueprint(availabilityBp)
app.register_blueprint(accountBp)
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
app.register_blueprint(playerAvailabilityCommentBp)
app.register_blueprint(paymentBp)
app.register_blueprint(profilBp)
app.register_blueprint(userBp)

# Création des tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)