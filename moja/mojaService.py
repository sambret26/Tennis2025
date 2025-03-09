import moja.mojaRequests as mojaRequests
import os

from models.Category import Category
from models.Court import Court
from models.Grid import Grid
from models.Ranking import Ranking
from models.Match import Match
#from models.Competition import Competition

from repositories.CategoryRepository import CategoryRepository
from repositories.CourtRepository import CourtRepository
from repositories.GridRepository import GridRepository
from repositories.SettingRepository import SettingRepository
from repositories.RankingRepository import RankingRepository
from repositories.PlayerRepository import PlayerRepository
from repositories.PlayerAvailabilityCommentRepository import PlayerAvailabilityCommentRepository
from repositories.PlayerBalanceRepository import PlayerBalanceRepository
from repositories.PlayerAvailabilityRepository import PlayerAvailabilityRepository
from repositories.PaymentRepository import PaymentRepository
from repositories.PlayerCategoriesRepository import PlayerCategoriesRepository
from repositories.ReductionRepository import ReductionRepository
from repositories.TransactionRepository import TransactionRepository
from repositories.MatchRepository import MatchRepository
from repositories.CompetitionRepository import CompetitionRepository
from repositories.UrlRepository import UrlRepository

from logger.logger import log, BATCH

categoryRepository = CategoryRepository()
courtRepository = CourtRepository()
gridRepository = GridRepository()
settingRepository = SettingRepository()
rankingRepository = RankingRepository()
playerRepository = PlayerRepository()
playerAvailabilityCommentRepository = PlayerAvailabilityCommentRepository()
playerBalanceRepository = PlayerBalanceRepository()
playerAvailabilityRepository = PlayerAvailabilityRepository()
paymentRepository = PaymentRepository()
playerCategoriesRepository = PlayerCategoriesRepository()
reductionRepository = ReductionRepository()
transactionRepository = TransactionRepository()
matchRepository = MatchRepository()
competitionRepository = CompetitionRepository()
urlRepository = UrlRepository()

def getCategoryDataUrl(categoryId):
    categoryUrl = urlRepository.getUrlByLabel("CategoryData")
    return categoryUrl.replace("CATEGORY_ID", str(categoryId))

def getCompetitionsDataUrl():
    competitionUrl = urlRepository.getUrlByLabel("Competition")
    return competitionUrl.replace("JA_ID", str(settingRepository.getJaId()))

def getCategoryInfos(categoryId):
    return mojaRequests.sendGetRequest(getCategoryDataUrl(categoryId))

def getGridDataUrl(gridId):
    gridUrl = urlRepository.getUrlByLabel("GridData")
    return gridUrl.replace("GRID_ID", str(gridId))

def getCompetitions():
    return mojaRequests.sendGetRequest(getCompetitionsDataUrl())

def updateCompetitions():
    competitionsToAdd = []
    jaId = settingRepository.getJaId()
    competitionUrl = urlRepository.getUrlByLabel("Competition").replace("JA_ID", str(jaId))
    competitions = mojaRequests.sendGetRequest(competitionUrl)
    for competition in competitions:
        competitionsToAdd.append(Competition.fromFFT(competition))
    competitionRepository.addCompetitions(competitionsToAdd)

def updateHomologation():
    log.info(BATCH, "Suppression de toutes les données")
    playerAvailabilityRepository.deleteAllPlayerAvailabilities()
    playerAvailabilityCommentRepository.deleteAllPlayerAvailabilityComments()
    playerBalanceRepository.deleteAllPlayerBalances()
    playerCategoriesRepository.deleteAllPlayerCategories()
    reductionRepository.deleteAllReductions()
    paymentRepository.deleteAllPayments()
    playerRepository.deleteAllPlayers()
    transactionRepository.deleteAllTransactions()
    competition = getHomologationInfos()
    if competition:
        log.info(BATCH, "Mise à jour des courts")
        updateCourtsInDB(competition["courts"])
        log.info(BATCH, "Mise à jour des dates")
        updateDates(competition)
    log.info(BATCH, "Mise à jour des catégories")
    updateCategories()
    for category in categoryRepository.getAllCategories():
        log.info(BATCH, "Mise à jour des découpages de la catégorie " + category.code)
        updateGrid(category.id, category.fftId)
    updateAllMatches()
    log.info(BATCH, "Mise à jour des classements")
    updateRankings()
    return 200

def getHomologationInfos():
    homologationId = competitionRepository.getHomologationId()
    jaId = settingRepository.getJaId()
    competitionUrl = urlRepository.getUrlByLabel("Competition").replace("JA_ID", str(jaId))
    response = mojaRequests.sendGetRequest(competitionUrl)
    if response == None:
        return None
    for competition in response["competitions"]:
        if int(competition["homologationId"]) == int(homologationId):
            return competition
    return None

def updateCourts():
    competition = getHomologationInfos()
    if competition == None:
        return None
    courts = competition["courts"]
    updateCourtsInDB(courts)
    return 200

def updateCourtsInDB(courts):
    courtsToAdd = []
    for court in courts:
        courtsToAdd.append(Court.fromFFT(court))
    if courtsToAdd != []:
        courtRepository.deleteAllCourts()
        courtRepository.addCourts(courtsToAdd)

def updateDates(competition):
    format = "%Y-%m-%d"
    settingRepository.setStartDate(competition["dateDebutHomologation"].split('T')[0])
    settingRepository.setEndDate(competition["dateFinHomologation"].split('T')[0])

def updateCategories():
    homologationId = competitionRepository.getHomologationId()
    categoriesUrl = urlRepository.getUrlByLabel("Category").replace("HOMOLOGATION_ID", str(homologationId))
    categories = mojaRequests.sendGetRequest(categoriesUrl)
    if categories == None:
        return None
    categoriesToAdd = []
    for category in categories:
        newCategory = Category.fromFFT(category)
        newCategory.amount = 17 #TODO
        categoriesToAdd.append(newCategory)
    if categoriesToAdd != []:
        gridRepository.deleteAllGrids()
        categoryRepository.deleteAllCategories()
        categoryRepository.addCategories(categoriesToAdd)
    return 200

def updateAllMatches():
    result = 200
    for grid in gridRepository.getAllGrids():
        log.info(BATCH, "Mise à jour des matches de la grille " + grid.name)
        if updateMatches(grid.id, grid.tableId, grid.categoryId) == 404:
            result = 404
    return result

def updateGrid(categoryId, categoryFftId):  
    categoryInfos = getCategoryInfos(categoryFftId)
    if categoryInfos == None: return 404
    gridsToAdd = []
    grids = categoryInfos["decoupageDisplayList"]
    for grid in grids :
        newGrid = Grid.fromFFT(grid)
        newGrid.categoryId = categoryId
        gridsToAdd.append(newGrid)
    if gridsToAdd != []:
        gridRepository.deleteAllGridsByCategory(categoryId)
        gridRepository.addGrids(gridsToAdd)
    return 200

def updateMatches(gridId, gridFftId, categoryId):
    url = getGridDataUrl(gridFftId)
    matches = mojaRequests.sendGetRequest(url)
    if matches == None: return 404
    matchesToAdd = []
    for match in matches:
        matchesToAdd.append(createMatch(match, categoryId, gridId))
    if matchesToAdd != []:
        matchRepository.deleteAllMatchesByGrid(gridId)
        matchRepository.addMatches(matchesToAdd)
    return 200

def updateRankings():
    categories = categoryRepository.getAllCategories()
    rankingsToAdd = []
    for category in categories:
        categoryInfos = getCategoryInfos(category.fftId)
        if categoryInfos == None: continue
        rankings = categoryInfos["classementList"]
        if rankings == None: continue
        addRankings(rankingsToAdd, rankings)
    playerRepository.deleteAllPlayers()
    rankingRepository.deleteAllRankings()
    rankingRepository.addRankings(rankingsToAdd)
    return 200

def createMatch(match, categoryId, gridId):
    newMatch = Match.fromFFT(match)
    newMatch.player1Id = getPlayerId(match['joueurList'], 0)
    newMatch.player2Id = getPlayerId(match['joueurList'], 1)
    newMatch.team1Id = None #TODO
    newMatch.team2Id = None #TODO
    newMatch.double = match["nomCategorie"].startswith("D")
    newMatch.categoryId = categoryId
    newMatch.gridId = gridId
    return newMatch

def addRankings(rankingsToAdd, rankings):
    for ranking in rankings:
        newRanking = Ranking.fromFFT(ranking)
        if newRanking != None and newRanking not in rankingsToAdd :
            rankingsToAdd.append(newRanking)

def getPlayerId(list, i):
    fftId = list[i]['joueurId'] if len(list) > i else None
    if fftId == None: return None
    player = playerRepository.getPlayerByFftId(fftId)
    if player == None: return None
    return player.id

