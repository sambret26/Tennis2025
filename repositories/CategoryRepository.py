from models.Category import Category
from database import db

class CategoryRepository:

    @staticmethod
    def addCategory(category):
        db.session.add(category)
        db.session.commit()

    @staticmethod
    def addCategories(categories):
        db.session.add_all(categories)
        db.session.commit()

    @staticmethod
    def getAllCategories():
        return Category.query.all()

    @staticmethod
    def getCategoryById(categoryId):
        return Category.query.get(categoryId)

    @staticmethod
    def getCategoryByCode(code):
        return Category.query.filter_by(code=code).first()

    @staticmethod
    def getCategoryIdByFftId(fftId):
        return Category.query.filter_by(fftId=fftId).first().id

    @staticmethod
    def deleteAllCategories():
        Category.query.delete()
        db.session.commit()