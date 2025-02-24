from models.ReductionSettings import ReductionSettings
from database import db

class ReductionSettingsRepository:

    #GETTERS
    @staticmethod
    def getAllReductionSettings():
        return ReductionSettings.query.all()

    @staticmethod
    def getReductionSettingById(reductionSettingId):
        return ReductionSettings.query.get(reductionSettingId)

    #ADDERS
    @staticmethod
    def addReductionSetting(reductionSetting):
        db.session.add(reductionSetting)
        db.session.commit()

    @staticmethod
    def addReductionSettings(reductionSettings):
        db.session.add_all(reductionSettings)
        db.session.commit()

    #SETTERS
    @staticmethod
    def updateReductionSetting(reductionSetting):
        ReductionSettings.query.filter_by(id=reductionSetting.id).update(reductionSetting.toDict())
        db.session.commit()

    #DELETERS
    @staticmethod
    def deleteByIdNoIn(idToSave):
        ReductionSettings.query.filter(ReductionSettings.id.notin_(idToSave)).delete()
        db.session.commit()