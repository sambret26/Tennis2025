from flask import Blueprint
from repositories.PlayerCategoriesRepository import PlayerCategoriesRepository

playerCategoriesRepository = PlayerCategoriesRepository()

playerCategoriesBp = Blueprint('playerCategoriesBp', __name__, url_prefix='/playerCategories')