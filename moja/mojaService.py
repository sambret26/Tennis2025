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
from repositories.TeamRepository import TeamRepository

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
teamRepository = TeamRepository()

def getCategoryDataUrl(categoryId):
    categoryUrl = urlRepository.getUrlByLabel("CategoryData")
    return categoryUrl.replace("CATEGORY_ID", str(categoryId))

def getCompetitionsDataUrl():
    competitionUrl = urlRepository.getUrlByLabel("Competition")
    return competitionUrl.replace("JA_ID", str(settingRepository.getJaId()))

def getCategoryInfos(categoryId):
    return mojaRequests.sendGetRequest(getCategoryDataUrl(categoryId))

def getGridDataUrl(gridTableId):
    gridUrl = urlRepository.getUrlByLabel("GridData")
    return gridUrl.replace("GRID_ID", str(gridTableId))

def getGridDataUrlPoule(gridFftId):
    gridUrl = urlRepository.getUrlByLabel("GridDataPoule")
    return gridUrl.replace("GRID_ID", str(gridFftId))

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
        updateCourtsInDB(competition["courts"])
    updateCategories()
    for category in categoryRepository.getAllCategories():
        updateGrid(category.id, category.fftId)
    updateAllMatches()
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
    report = UpdatedMatchReport(0, 0, 0)
    result = 200
    oldCategory = None
    matchIndex = 1
    for grid in gridRepository.getAllGrids():
        if oldCategory != grid.categoryId: matchIndex = 1
        matchAdded = updateMatches(grid.category.code, grid, matchIndex, report)
        if matchAdded == 404: result = 404
        matchIndex += matchAdded
        oldCategory = grid.categoryId
    message = report.createMessage()
    log.info(BATCH, message)
    return result

def updateGrids():
    for category in categoryRepository.getAllCategories():
        updateGrid(category.id, category.fftId)

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

def updateMatches(categoryCode, grid, matchIndex, report):
    matchsIdtoDelete = matchRepository.getAllMatchesIdByGrid(grid.id)
    newMatchs = []
    matches = []
    courtsMap = courtRepository.getCourtsMap()
    if grid.type == "POU":
        url = getGridDataUrlPoule(grid.fftId)
    else:
        url = getGridDataUrl(grid.tableId)
    matchesFromFFT = mojaRequests.sendGetRequest(url)
    if matchesFromFFT == None: return 404
    if grid.type != "POU" :
        sortedMatchs = sorted(matchesFromFFT, key=lambda x: (int(x["numeroMatch"][3]), int(x["numeroMatch"][1]), int(x["numeroMatch"][5])))
    else:
        sortedMatchs = matchesFromFFT
    for match in sortedMatchs:
        newMatch = createMatch(match, grid.categoryId, grid.id, courtsMap, categoryCode, matchIndex)
        matches.append(newMatch)
        matchIndex += 1
    for match in matches:
        matchInDB = matchRepository.getMatchByFftId(match.fftId)
        if matchInDB:
            if match.isDifferent(matchInDB):
                match.id = matchInDB.id
                report.updated += 1
                matchRepository.updateMatchFromBatch(match)
            matchsIdtoDelete.remove(matchInDB.id)
        else:
            newMatchs.append(match)
    if newMatchs != []: matchRepository.addMatches(newMatchs)
    matchRepository.deleteMatches(matchsIdtoDelete)
    report.added += len(newMatchs)
    report.deleted += len(matchsIdtoDelete)
    return len(matches)

def updateRankings():
    categories = categoryRepository.getAllCategories()
    rankingsToAdd = []
    for category in categories:
        categoryInfos = getCategoryInfos(category.fftId)
        if categoryInfos == None: continue
        rankings = categoryInfos["classementList"]
        if rankings == None: continue
        addRankings(category.code, rankingsToAdd, rankings)
    playerRepository.deleteAllPlayers()
    rankingRepository.deleteAllRankings()
    rankingRepository.addRankings(rankingsToAdd)
    return 200

def createMatch(match, categoryId, gridId, courtsMap, categoryCode, matchIndex):
    newMatch = Match.fromFFT(match)
    newMatch.categoryId = categoryId
    newMatch.gridId = gridId
    newMatch.double = match["nomCategorie"].startswith("D")
    newMatch.courtId = courtsMap.get(int(match['courtId'])) if match['courtId'] != None else None
    newMatch.label = categoryCode + str(matchIndex).zfill(2)
    setPlayersOrTeam(newMatch, match)
    setWinner(newMatch, match)
    setProgrammation(newMatch, match)
    return newMatch

def setPlayersOrTeam(match, matchData):
    if match.double:
        match.team1Id = getTeamId(matchData['joueurList'], 0)
        match.team2Id = getTeamId(matchData['joueurList'], 1)
    else:
        match.player1Id = getPlayerId(matchData['joueurList'], 0)
        match.player2Id = getPlayerId(matchData['joueurList'], 1)

def setWinner(match, matchData):
    if matchData["equipeGagnante"] == None: return
    match.finish = True
    if match.double:
        if matchData["equipeGagnante"] == "equipeA":
            match.teamWinnerId = match.team1Id
        else:
            match.teamWinnerId = match.team2Id
    else:
        if matchData["equipeGagnante"] == "equipeA":
            match.winnerId = match.player1Id
        else:
            match.winnerId = match.player2Id
    setScore(match, matchData)

def setScore(match, matchData):
    score = ""
    for set in matchData["sets"]:
        if set["scoreA"] == 0 and set["scoreB"] == 0: break
        if score != "" : score += " "
        if matchData["equipeGagnante"] == "equipeA":
            score += str(set["scoreA"]) + "/" + str(set["scoreB"])
        else:
            score += str(set["scoreB"]) + "/" + str(set["scoreA"])
        if set["tieBreak"] != None:
            score += "(" + str(set["tieBreak"]) + ")"
    match.score = score

def setProgrammation(match, matchData):
    if matchData["dateProgrammation"] and "T" in matchData["dateProgrammation"]:
        match.day = matchData["dateProgrammation"].split("T")[0]
        match.hour = matchData["dateProgrammation"].split("T")[1][:5]

def addRankings(categoryCode, rankingsToAdd, rankings):
    for ranking in rankings:
        if categoryCode.startswith("S"):
            newRanking = Ranking.fromFFTSimple(ranking)
        else:
            newRanking = Ranking.fromFFTDouble(ranking)
        if newRanking != None and newRanking not in rankingsToAdd :
            rankingsToAdd.append(newRanking)

def getPlayerId(list, i):
    fftId = list[i]['joueurId'] if len(list) > i else None
    if fftId == None: return None
    player = playerRepository.getPlayerByFftId(fftId)
    if player == None: return None
    return player.id

def getTeamId(list, i):
    if i == 0 :
        fftId1 = list[0]['joueurId'] if len(list) > 0 else None
        fftId2 = list[1]['joueurId'] if len(list) > 1 else None
    else :
        fftId1 = list[2]['joueurId'] if len(list) > 2 else None
        fftId2 = list[3]['joueurId'] if len(list) > 3 else None
    if fftId1 == None or fftId2 == None: return None
    player1Id = playerRepository.getPlayerByFftId(fftId1).id
    player2Id = playerRepository.getPlayerByFftId(fftId2).id
    team = teamRepository.getTeamByPlayersIds(player1Id, player2Id)
    if team == None: return None
    return team.id

class UpdatedMatchReport:
    def __init__(self, updated, added, deleted):
        self.updated = updated
        self.added = added
        self.deleted = deleted

    def createMessage(self):
        return f"Nombre de matchs mis à jour : {self.updated} | Nombre de matchs ajoutés : {self.added} | Nombre de matchs supprimés : {self.deleted}"