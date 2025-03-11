from flask import Blueprint, jsonify, request
from repositories.CompetitionRepository import CompetitionRepository
from services.business import CompetitionBusiness
from models.Competition import Competition
from repositories.SettingRepository import SettingRepository
import moja.mojaService as mojaService
import batchs.batchs as batchs

competitionRepository = CompetitionRepository()
settingRepository = SettingRepository()

competitionBp = Blueprint('competitionBp', __name__, url_prefix='/competitions')

@competitionBp.route('/', methods=['GET'])
def getCompetitions():
    competitions = competitionRepository.getCompetitions()
    return jsonify([competition.toDict() for competition in competitions]), 200

@competitionBp.route('/', methods=['POST'])
def addCompetition():
    competition = Competition.fromJson(request.json)
    competitionRepository.addCompetition(competition)
    return jsonify({'message': 'Competition added successfully!'}), 201

@competitionBp.route('/', methods=['PUT'])
def updateCompetition():
    competition = Competition.fromJson(request.json)
    competitionRepository.updateCompetition(competition)
    return jsonify({'message': 'Competition updated successfully!'}), 200

@competitionBp.route('/', methods=['DELETE'])
def deleteCompetition():
    competition = Competition.fromJson(request.json)
    competitionRepository.deleteCompetition(competition)
    return jsonify({'message': 'Competition deleted successfully!'}), 200

@competitionBp.route('/update', methods=['POST'])
def updateCompetitions():
    result = CompetitionBusiness.updateCompetitions()
    if result == None:
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
    if (isBatchActive):
        settingRepository.setBatchsActive("0")
    competitionId = request.json
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