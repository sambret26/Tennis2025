from models.User import User
from sqlalchemy import func, or_
from database import db

class UserRepository:

    @staticmethod
    def getUserByName(name):
        return User.query.filter(func.lower(User.name) == name.lower()).first()

    @staticmethod
    def getUserById(userId):
        return User.query.filter_by(id=userId).first()

    @staticmethod
    def updateProfile(userId, newRole, superAdmin):
        User.query.filter_by(id=userId).update({"profileValue": newRole, "superAdmin": superAdmin})
        db.session.commit()
        user = User.query.filter_by(id=userId).first()
        return user

    @staticmethod
    def updatePassword(userId, password):
        User.query.filter_by(id=userId).update({"password": password})
        db.session.commit()

    @staticmethod
    def addUser(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def getAdminWithPassword(password):
        return User.query.filter(User.password==password, or_(User.profileValue==2, User.superAdmin==1)).first()