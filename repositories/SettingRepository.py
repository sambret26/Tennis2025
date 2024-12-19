import stat
from models.Setting import Setting
from database import db

class SettingRepository:

    @staticmethod
    def addSetting(setting):
        db.session.add(setting)
        db.session.commit()

    @staticmethod
    def addSettings(settings):
        db.session.addAll(settings)
        db.session.commit()

    @staticmethod
    def getAllSettings():
        return Setting.query.all()

    @staticmethod
    def getSettingById(settingId):
        return Setting.query.get(settingId)

    @staticmethod
    def getDates():
        results = Setting.query.with_entities(
            Setting.value.label('value'), Setting.key.label('key')
        ).filter(Setting.key.in_(['startDate', 'endDate'])).all()
        dates = {result.key: result.value for result in results}
        return dates
