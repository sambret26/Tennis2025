from flask import Blueprint, jsonify, request
from repositories.SettingRepository import SettingRepository
from models.Setting import Setting

settingRepository = SettingRepository()

settingBp = Blueprint('settingBp', __name__, url_prefix='/settings')

@settingBp.route('/', methods=['GET'])
def getSettings():
    settings = settingRepository.getAllSettings()
    settingsDict = {setting.key: setting.value for setting in settings}
    return jsonify(settingsDict), 200

@settingBp.route('/', methods=['POST'])
def addSetting():
    setting = Setting.fromJson(request.json)
    settingRepository.addSetting(setting)
    return jsonify({'message': 'Setting added successfully!'}), 201

@settingBp.route('/batchsActive', methods=['PUT'])
def setBatchsActive():
    batchsActive = request.json['batchsActive']
    settingRepository.setBatchsActive(batchsActive)
    return jsonify({'message': 'Batchs active updated successfully!'}), 200

@settingBp.route('/mojaSync', methods=['PUT'])
def setMojaSync():
    mojaSync = request.json['mojaSync']
    settingRepository.setMojaSync(mojaSync)
    return jsonify({'message': 'Moja sync updated successfully!'}), 200

@settingBp.route('/calendarSync', methods=['PUT'])
def setCalendarSync():
    calendarSync = request.json['calendarSync']
    settingRepository.setCalendarSync(calendarSync)
    return jsonify({'message': 'Calendar sync updated successfully!'}), 200

@settingBp.route('/updatePrices', methods=['PUT'])
def updatePrices():
    prices = request.json
    settingRepository.updatePrices(prices)
    return jsonify({'message': 'Prices updated successfully!'}), 200