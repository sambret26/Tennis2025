from models.ReductionSettings import ReductionSettings
from database import db

class ReductionSettingsRepository:

    @staticmethod
    def addReductionSetting(reductionSetting):
        db.session.add(reductionSetting)
        db.session.commit()

    @staticmethod
    def getAllReductionSettings():
        return ReductionSettings.query.all()

    @staticmethod
    def getReductionSettingById(reductionSettingId):
        return ReductionSettings.query.get(reductionSettingId)