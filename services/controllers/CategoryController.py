from flask import Blueprint, jsonify, request
from repositories.CategoryRepository import CategoryRepository
from models.Category import Category

categoryRepository = CategoryRepository()

categoryBp = Blueprint('categoryBp', __name__, url_prefix='/categories')

@categoryBp.route('/', methods=['GET'])
def getCategories():
    categories = categoryRepository.getAllCategories()
    return jsonify([category.toDict() for category in categories]), 200

@categoryBp.route('/', methods=['POST'])
def addCategory():
    category = Category.fromJson(request.json)
    categoryRepository.addCategory(category)
    return jsonify({'message': 'Category added successfully!'}), 201
