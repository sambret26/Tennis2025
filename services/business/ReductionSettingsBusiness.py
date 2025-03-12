from repositories.ReductionSettingsRepository import ReductionSettingsRepository
from models.ReductionSettings import ReductionSettings

reductionSettingsRepository = ReductionSettingsRepository()

def update(reductionSettings):
    idToSave = []
    reductionToUpdate = []
    reductionToSave = []
    for reductionSetting in reductionSettings:
        reduction = ReductionSettings.fromJson(reductionSetting)
        reductionId = reductionSetting['id'] if 'id' in reductionSetting else None
        if reductionId is None:
            reductionToSave.append(reduction)
        else :
            idToSave.append(reductionId)
            reduction.id = reductionId
            reductionToUpdate.append(reduction)
    reductionSettingsRepository.deleteByIdNoIn(idToSave)
    reductionSettingsRepository.addReductionSettings(reductionToSave)
    for reductionSetting in reductionToUpdate:
        reductionSettingsRepository.updateReductionSetting(reductionSetting)