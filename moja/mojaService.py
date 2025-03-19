from moja import mojaRequests

from models.Category import Category
from models.Court import Court
from models.Grid import Grid
from models.Ranking import Ranking
from models.Match import Match
from constants import constants

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

def getHomologationInfos():
    homologationId = competitionRepository.getHomologationId()
    jaId = settingRepository.getJaId()
    competitionUrl = urlRepository.getUrlByLabel("Competition").replace("JA_ID", str(jaId))
    response = mojaRequests.sendGetRequest(competitionUrl)
    if response is None:
        return None
    for competition in response["competitions"]:
        if int(competition["homologationId"]) == int(homologationId):
            return competition
    return None

def updateCourts():
    competition = getHomologationInfos()
    if competition is None:
        return None
    courts = competition["courts"]
    updateCourtsInDB(courts)
    return 200

#TODO : Update instead of delete and add
def updateCourtsInDB(courts):
    courtsToAdd = []
    for court in courts:
        courtsToAdd.append(Court.fromFFT(court))
    if courtsToAdd:
        courtRepository.deleteAllCourts()
        courtRepository.addCourts(courtsToAdd)

#TODO : Update instead of delete and add
def updateCategories():
    categoriesPrices = settingRepository.getCategoriesPrices()
    homologationId = competitionRepository.getHomologationId()
    categoriesUrl = urlRepository.getUrlByLabel("Category")\
        .replace("HOMOLOGATION_ID", str(homologationId))
    categories = mojaRequests.sendGetRequest(categoriesUrl)
    if categories is None:
        return None
    categoriesToAdd = []
    for category in categories:
        newCategory = Category.fromFFT(category)
        if "(C)" in newCategory.label:
            newCategory.amount = 0
            newCategory.code = newCategory.code.replace("S", "C")
        elif newCategory.code.startswith("D"):
            newCategory.amount = categoriesPrices['doublePrice']
        else :
            newCategory.amount = categoriesPrices['simplePrice']
        categoriesToAdd.append(newCategory)
    if categoriesToAdd:
        gridRepository.deleteAllGrids()
        categoryRepository.deleteAllCategories()
        categoryRepository.addCategories(categoriesToAdd)
    return 200

def updateAllMatches():
    courtsMap = courtRepository.getCourtsMap()
    playersIdMap = playerRepository.getPlayersIdMap()
    matchesMap = matchRepository.getMatchesMap()
    report = UpdatedMatchReport(0, 0, 0)
    result = 200
    oldCategory = None
    matchIndex = 1
    newMatchs = []
    playersInfo = []
    for grid in gridRepository.getAllGrids():
        if oldCategory != grid.categoryId:
            matchIndex = 1
        matchAdded = updateMatches(newMatchs, matchesMap, grid, matchIndex, report, courtsMap, playersIdMap, playersInfo)
        if matchAdded == 404:
            result = 404
        matchIndex += matchAdded
        oldCategory = grid.categoryId
    if newMatchs:
        matchRepository.addMatches(newMatchs)
    if matchesMap:
        matchRepository.deleteMatches([m.id for m in matchesMap.values()])
        report.deleted += len(matchesMap)
    message = report.createMessage()
    updatePlayersInfos(playersInfo)
    log.info(BATCH, message)
    return result

def updateGrids():
    for category in categoryRepository.getAllCategories():
        updateGrid(category.id, category.fftId)

#TODO : Update instead of delete and add
def updateGrid(categoryId, categoryFftId):
    categoryInfos = getCategoryInfos(categoryFftId)
    if categoryInfos is None:
        return 404
    gridsToAdd = []
    grids = categoryInfos["decoupageDisplayList"]
    for grid in grids :
        newGrid = Grid.fromFFT(grid)
        newGrid.categoryId = categoryId
        gridsToAdd.append(newGrid)
    if gridsToAdd:
        gridRepository.deleteAllGridsByCategory(categoryId)
        gridRepository.addGrids(gridsToAdd)
    return 200

def updateMatches(newMatchs, matchesMap, grid, matchIndex, report, courtsMap, playersIdMap, playersInfo):
    matches = []
    if grid.type == "POU":
        url = getGridDataUrlPoule(grid.fftId)
    else:
        url = getGridDataUrl(grid.tableId)
    matchesFromFFT = mojaRequests.sendGetRequest(url)
    if matchesFromFFT is None:
        return 404
    if grid.type != "POU" :
        sortedMatchs = sorted(matchesFromFFT, key=lambda x: tuple(int(x["numeroMatch"][i]) for i in [3, 1, 5]))
    else:
        sortedMatchs = matchesFromFFT
    for match in sortedMatchs:
        newMatch = createMatch(match, grid, courtsMap, grid.category.code, matchIndex, playersIdMap)
        getPlayersInfos(match, playersInfo)
        matches.append(newMatch)
        matchIndex += 1
    for match in matches:
        matchInDB = matchesMap.get(match.fftId)
        if matchInDB:
            if match.isDifferent(matchInDB):
                match.id = matchInDB.id
                report.updated += 1
                matchRepository.updateMatchFromBatch(match)
            matchesMap.pop(match.fftId)
        else:
            newMatchs.append(match)
            report.added += 1
    return len(matches)

#TODO : Update instead of delete and add
def updateRankings():
    categories = categoryRepository.getAllCategories()
    rankingsToAdd = []
    for category in categories:
        categoryInfos = getCategoryInfos(category.fftId)
        if categoryInfos is None:
            continue
        rankings = categoryInfos["classementList"]
        if rankings is None:
            continue
        addRankings(category.code, rankingsToAdd, rankings)
    playerRepository.deleteAllPlayers()
    rankingRepository.deleteAllRankings()
    rankingRepository.addRankings(rankingsToAdd)
    return 200

def createMatch(match, grid, courtsMap, categoryCode, matchIndex, playersIdMap):
    newMatch = Match.fromFFT(match)
    newMatch.categoryId = grid.categoryId
    newMatch.gridId = grid.id
    newMatch.double = match["nomCategorie"].startswith("D")
    newMatch.courtId = courtsMap.get(int(match['courtId'])) if match['courtId'] is not None else None
    newMatch.label = categoryCode + str(matchIndex).zfill(2)
    setPlayersOrTeam(newMatch, match, playersIdMap)
    setWinner(newMatch, match)
    setProgrammation(newMatch, match)
    return newMatch

def setPlayersOrTeam(match, matchData, playersIdMap):
    if match.double:
        match.team1Id = getTeamId(matchData['joueurList'], 0, playersIdMap)
        match.team2Id = getTeamId(matchData['joueurList'], 1, playersIdMap)
    else:
        match.player1Id = getPlayerId(matchData['joueurList'], 0, playersIdMap)
        match.player2Id = getPlayerId(matchData['joueurList'], 1, playersIdMap)

def setWinner(match, matchData):
    if matchData["equipeGagnante"] is None:
        return
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
        if set["scoreA"] == 0 and set["scoreB"] == 0:
            break
        if score != "":
            score += " "
        if matchData["equipeGagnante"] == "equipeA":
            score += str(set["scoreA"]) + "/" + str(set["scoreB"])
        else:
            score += str(set["scoreB"]) + "/" + str(set["scoreA"])
        if set["tieBreak"] is not None:
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
        if newRanking is not None and newRanking not in rankingsToAdd :
            rankingsToAdd.append(newRanking)

def getPlayerId(playersList, i, playersIdMap):
    fftId = int(playersList[i]['joueurId']) if len(playersList) > i else None
    if fftId is None:
        return None
    return playersIdMap.get(fftId)

def getTeamId(playersList, i, playersIdMap):
    if i == 0 :
        fftId1 = int(playersList[0]['joueurId']) if len(playersList) > 0 else None
        fftId2 = int(playersList[1]['joueurId']) if len(playersList) > 1 else None
    else :
        fftId1 = int(playersList[2]['joueurId']) if len(playersList) > 2 else None
        fftId2 = int(playersList[3]['joueurId']) if len(playersList) > 3 else None
    if fftId1 is None or fftId2 is None:
        return None
    player1Id = playersIdMap.get(fftId1)
    player2Id = playersIdMap.get(fftId2)
    team = teamRepository.getTeamByPlayersIds(player1Id, player2Id)
    if team is None:
        return None
    return team.id

def getPlayersInfos(match, playersInfo):
    for player in match['joueurList']:
        fftId = int(player['joueurId'])
        email = player['mail']
        phoneNumber = player['numTel']
        playersInfo.append(PlayersInfos(fftId, email, phoneNumber))

def updatePlayersInfos(playersInfo):
    players = playerRepository.getPlayersMap()
    for playerInfo in playersInfo:
        player = players.get(playerInfo.fftId)
        if player is None :
            continue
        if player.email == playerInfo.email and player.phoneNumber == playerInfo.phoneNumber:
            continue
        player.email = playerInfo.email
        player.phoneNumber = playerInfo.phoneNumber
        playerRepository.updatePlayerFromBatch(player)

class PlayersInfos:
    def __init__(self, fftId, email, phoneNumber):
        self.fftId = fftId
        self.email = email
        self.phoneNumber = phoneNumber

class UpdatedMatchReport:
    def __init__(self, updated, added, deleted):
        self.updated = updated
        self.added = added
        self.deleted = deleted

    def createMessage(self):
        return f"{constants.ADD_MATCHES}{self.added}\
            | {constants.UPDATE_MATCHES}{self.updated}\
            | {constants.DELETE_MATCHES}{self.deleted}"