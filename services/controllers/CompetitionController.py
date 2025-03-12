from flask import Blueprint, jsonify, request
from repositories.CompetitionRepository import CompetitionRepository
from repositories.SettingRepository import SettingRepository
from services.business import CompetitionBusiness
from  moja import mojaService
from  batchs import batchs

competitionRepository = CompetitionRepository()
settingRepository = SettingRepository()

competitionBp = Blueprint('competitionBp', __name__, url_prefix='/competitions')

@competitionBp.route('/', methods=['GET'])
def getCompetitions():
    competitions = competitionRepository.getCompetitions()
    return jsonify([competition.toDict() for competition in competitions]), 200

@competitionBp.route('/update', methods=['POST'])
def updateCompetitions():
    result = CompetitionBusiness.updateCompetitions()
    if result is None:
        return jsonify({'message': 'No competitions found!'}), 404
    return jsonify({'message': 'Competitions updated successfully!'}), 200

@competitionBp.route('/dates', methods=['GET'])
def getDates():
    dates =  competitionRepository.getDates()
    if dates == (None, None):
        return jsonify({'message': 'No competitions found!'}), 404
    return jsonify({'startDate': dates[0], 'endDate': dates[1]}), 200

@competitionBp.route('/active', methods=['PUT'])
def activeCompetition():
    isBatchActive = settingRepository.getBatchsActive()
    if isBatchActive:
        settingRepository.setBatchsActive("0")
    competitionId = request.json['competitionId']
    competitionRepository.setInactive()
    competitionRepository.setActive(competitionId)
    return jsonify({'message': 'Competition updated successfully!', 'isBatchActive': isBatchActive}), 200

@competitionBp.route('/deleteAllDatas', methods=['DELETE'])
def deleteData():
    CompetitionBusiness.deleteData()
    return jsonify({'message': 'Data deleted successfully!'}), 200

@competitionBp.route('/courts', methods=['POST'])
def updateCourts():
    mojaService.updateCourts()
    return jsonify({'message': 'Courts updated successfully!'}), 200

@competitionBp.route('/categories', methods=['POST'])
def updateCategories():
    mojaService.updateCategories()
    return jsonify({'message': 'Categories updated successfully!'}), 200

@competitionBp.route('/grids', methods=['POST'])
def updateGrids():
    mojaService.updateGrids()
    return jsonify({'message': 'Grids updated successfully!'}), 200

@competitionBp.route('/matches', methods=['POST'])
def updateMatches():
    mojaService.updateAllMatches()
    return jsonify({'message': 'Matches updated successfully!'}), 200

@competitionBp.route('/rankings', methods=['POST'])
def updateRankings():
    mojaService.updateRankings()
    return jsonify({'message': 'Rankings updated successfully!'}), 200

@competitionBp.route('/players', methods=['POST'])
def updatePlayers():
    batchs.inscriptions(False)
    return jsonify({'message': 'Players updated successfully!'}), 200