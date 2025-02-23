from models.Setting import Setting
from database import db

class SettingRepository:

    @staticmethod
    def addSetting(setting):
        db.session.add(setting)
        db.session.commit()

    @staticmethod
    def addSettings(settings):
        db.session.add_all(settings)
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

    @staticmethod
    def getHomologationId():
        return Setting.query.filter(Setting.key == 'homologationId').first().value

    @staticmethod
    def getJaId():
        return Setting.query.filter(Setting.key == 'jaId').first().value

    @staticmethod
    def getBatchsActive():
        return Setting.query.filter(Setting.key == 'batchsActive').first().value == "1"

    @staticmethod
    def setStartDate(date):
        db.session.query(Setting).filter(Setting.key == 'startDate').update({Setting.value: date})
        db.session.commit()

    @staticmethod
    def setEndDate(date):
        db.session.query(Setting).filter(Setting.key == 'endDate').update({Setting.value: date})
        db.session.commit()

    @staticmethod
    def setBatchsActive(batchsActive):
        db.session.query(Setting).filter(Setting.key == 'batchsActive').update({Setting.value: batchsActive})
        db.session.commit()