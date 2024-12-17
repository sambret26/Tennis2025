from models.Category import Category
from database import db

class CategoryRepository:

    @staticmethod
    def addCategory(category):
        db.session.add(category)
        db.session.commit()

    @staticmethod
    def getAllCategories():
        return Category.query.all()

    @staticmethod
    def getCategoryById(categoryId):
        return Category.query.get(categoryId)