from flask import Blueprint, jsonify, request
from repositories.SettingRepository import SettingRepository
from models.Setting import Setting

settingBp = Blueprint('settingBp', __name__, url_prefix='/settings')

@settingBp.route('/', methods=['GET'])
def getSettings():
    settings = SettingRepository.getAllSettings()
    return jsonify([setting.toDict() for setting in settings]), 200

@settingBp.route('/', methods=['POST'])
def addSetting():
    setting = Setting.fromJson(request.json)
    SettingRepository.addSetting(setting)
    return jsonify({'message': 'Setting added successfully!'}), 201

@settingBp.route('/multiple', methods=['POST'])
def addSettings():
    settings = []
    for data in request.json:
        settings.append(Setting.fromJson(data))
    SettingRepository.addSettings(settings)
    return jsonify({'message': 'Settings added successfully!'}), 201