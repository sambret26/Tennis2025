from flask import Blueprint, jsonify, request
from repositories.ReductionSettingsRepository import ReductionSettingsRepository
from services.business import ReductionSettingsBusiness

reductionSettingsRepository = ReductionSettingsRepository()

reductionSettingsBp = Blueprint('reductionSettingsBp', __name__, url_prefix='/reductionSettings')

@reductionSettingsBp.route('/', methods=['GET'])
def getreductionSettings():
    reductionSettings = reductionSettingsRepository.getAllReductionSettings()
    return jsonify([reductionSetting.toDict() for reductionSetting in reductionSettings]), 200

@reductionSettingsBp.route('/update', methods=['PUT'])
def updatereductionSetting():
    reductionsSettings = request.json['reductions']
    ReductionSettingsBusiness.update(reductionsSettings)
    return jsonify({'message': 'Reduction setting updated successfully!'}), 200