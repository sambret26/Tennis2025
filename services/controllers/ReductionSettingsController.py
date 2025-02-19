from flask import Blueprint, jsonify, request
from repositories.ReductionSettingsRepository import ReductionSettingsRepository
from models.ReductionSettings import ReductionSettings

reductionSettingsRepository = ReductionSettingsRepository()

reductionSettingsBp = Blueprint('reductionSettingsBp', __name__, url_prefix='/reductionSettings')

@reductionSettingsBp.route('/', methods=['GET'])
def getreductionSettings():
    reductionSettings = reductionSettingsRepository.getAllReductionSettings()
    return jsonify([reductionSetting.toDict() for reductionSetting in reductionSettings]), 200

@reductionSettingsBp.route('/', methods=['POST'])
def addreductionSetting():
    reductionSetting = ReductionSettings.fromJson(request.json)
    reductionSettingsRepository.addreductionSetting(reductionSetting)
    return jsonify({'message': 'Reduction setting added successfully!'}), 201

@reductionSettingsBp.route('/multiple', methods=['POST'])
def addreductionSettings():
    reductionSettings = []
    for data in request.json:
        reductionSettings.append(ReductionSettings.fromJson(data))
    reductionSettingsRepository.addreductionSettings(reductionSettings)
    return jsonify({'message': 'Reduction settings added successfully!'}), 201