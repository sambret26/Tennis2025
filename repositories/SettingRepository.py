from models.Setting import Setting
from database import db

class SettingRepository:

    @staticmethod
    def addSetting(setting):
        db.session.add(setting)
        db.session.commit()

    @staticmethod
    def getAllSettings():
        return Setting.query.all()

    @staticmethod
    def getSettingById(settingId):
        return Setting.query.get(settingId)