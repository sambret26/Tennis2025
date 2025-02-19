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

@categoryBp.route('/multiple', methods=['POST'])
def addCategories():
    categories = []
    for data in request.json:
        categories.append(Category.fromJson(data))
    categoryRepository.addCategories(categories)
    return jsonify({'message': 'Categories added successfully!'}), 201