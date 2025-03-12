from flask import Blueprint
from repositories.CourtRepository import CourtRepository

courtRepository = CourtRepository()

courtBp = Blueprint('courtBp', __name__, url_prefix='/courts')