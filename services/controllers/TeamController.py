from flask import Blueprint
from repositories.TeamRepository import TeamRepository

teamRepository = TeamRepository()

teamBp = Blueprint('teamBp', __name__, url_prefix='/teams')