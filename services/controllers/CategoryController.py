from flask import Blueprint
from repositories.CategoryRepository import CategoryRepository

categoryRepository = CategoryRepository()

categoryBp = Blueprint('categoryBp', __name__, url_prefix='/categories')