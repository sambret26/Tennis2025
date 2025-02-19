from flask import Blueprint, jsonify, request
from repositories.SettingRepository import SettingRepository
from models.Setting import Setting

settingRepository = SettingRepository()

settingBp = Blueprint('settingBp', __name__, url_prefix='/settings')

@settingBp.route('/', methods=['GET'])
def getSettings():
    settings = settingRepository.getAllSettings()
    return jsonify([setting.toDict() for setting in settings]), 200

@settingBp.route('/dates', methods=['GET'])
def getDates():
    dates =  settingRepository.getDates()
    return jsonify({'startDate': dates['startDate'], 'endDate': dates['endDate']}), 200

@settingBp.route('/', methods=['POST'])
def addSetting():
    setting = Setting.fromJson(request.json)
    settingRepository.addSetting(setting)
    return jsonify({'message': 'Setting added successfully!'}), 201

@settingBp.route('/multiple', methods=['POST'])
def addSettings():
    settings = []
    for data in request.json:
        settings.append(Setting.fromJson(data))
    settingRepository.addSettings(settings)
    return jsonify({'message': 'Settings added successfully!'}), 201