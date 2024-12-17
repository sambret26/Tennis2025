from flask import Blueprint, jsonify, request
from repositories.ReductionSettingsRepository import ReductionSettingsRepository
from models.ReductionSettings import ReductionSettings

reductionSettingsBp = Blueprint('reductionSettingsBp', __name__, url_prefix='/reductionSettings')

@reductionSettingsBp.route('/', methods=['GET'])
def getreductionSettings():
    reductionSettings = ReductionSettingsRepository.getAllreductionSettings()
    return jsonify([reductionSetting.toDict() for reductionSetting in reductionSettings]), 200

@reductionSettingsBp.route('/', methods=['POST'])
def addreductionSetting():
    reductionSetting = ReductionSettings.fromJson(request.json)
    ReductionSettingsRepository.addreductionSetting(reductionSetting)
    return jsonify({'message': 'Reduction setting added successfully!'}), 201

@reductionSettingsBp.route('/multiple', methods=['POST'])
def addreductionSettings():
    reductionSettings = []
    for data in request.json:
        reductionSettings.append(ReductionSettings.fromJson(data))
    for reductionSetting in reductionSettings:
        ReductionSettingsRepository.addreductionSetting(reductionSetting)
    return jsonify({'message': 'Reduction settings added successfully!'}), 201