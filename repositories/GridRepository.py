from models.Grid import Grid
from database import db

class GridRepository:

    #GETTERS
    @staticmethod
    def getAllGrids():
        return Grid.query.order_by(Grid.categoryId).all()

    @staticmethod
    def getGridById(gridId):
        return Grid.query.get(gridId)

    #ADDERS
    @staticmethod
    def addGrid(grid):
        db.session.add(grid)
        db.session.commit()

    @staticmethod
    def addGrids(grids):
        db.session.add_all(grids)
        db.session.commit()

    #DELETERS
    @staticmethod
    def deleteAllGrids():
        Grid.query.delete()
        db.session.commit()

    @staticmethod
    def deleteAllGridsByCategory(categoryId):
        Grid.query.filter_by(categoryId=categoryId).delete()
        db.session.commit()