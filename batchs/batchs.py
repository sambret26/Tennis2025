
from models.Player import Player
from models.Team import Team
from models.Message import Message
from models.PlayerBalance import PlayerBalance
from models.PlayerCategories import PlayerCategories
from repositories.CategoryRepository import CategoryRepository
from repositories.PlayerRepository import PlayerRepository
from repositories.TeamRepository import TeamRepository
from repositories.RankingRepository import RankingRepository
from repositories.MessageRepository import MessageRepository
from repositories.PlayerBalanceRepository import PlayerBalanceRepository
from repositories.PlayerCategoriesRepository import PlayerCategoriesRepository
from moja import mojaService

playerRepository = PlayerRepository()
teamRepository = TeamRepository()
categoryRepository = CategoryRepository()
rankingRepository = RankingRepository()
messageRepository = MessageRepository()
playerBalanceRepository = PlayerBalanceRepository()
playerCategoriesRepository = PlayerCategoriesRepository()

def inscriptions(sendNotif):
    players, teams = getPlayersAndTeams()
    if players :
        updateDBPlayers(players, sendNotif)
    if teams :
        updateDBTeams(teams)

def updateMatch():
    return mojaService.updateAllMatches()

def updateCalendar():
    return None #TODO : Implement calendar batch

def getPlayersAndTeams():
    ranksMapSimple = rankingRepository.getRankingMapSimple()
    rankMapDouble = rankingRepository.getRankingMapDouble()
    categories = categoryRepository.getAllCategories()
    players = []
    teams = []
    for category in categories:
        datas = mojaService.getCategoryInfos(category.fftId)
        if not datas :
            return None, None
        for player in datas["listJoueurInscrit"]:
            if category.code.startswith("D"):
                addPlayersAndTeamInLists(players, teams, player, category, rankMapDouble)
            else:
                addPlayerInPlayersList(players, player, category, ranksMapSimple)
    return players, teams

def addPlayerInPlayersList(players, player, category, ranksMapSimple):
    newPlayer = Player.fromFFT(player)
    newPlayer.ranking = ranksMapSimple.get(player['classementJoueur1'])
    newPlayer.rankingId = newPlayer.ranking.id
    addPlayer(players, newPlayer, category)

def addPlayersAndTeamInLists(players, teams, team, category, rankMapDouble):
    newPlayer1 = Player.fromFFT(team)
    newPlayer2 = Player.fromFFT2(team)
    addPlayer(players, newPlayer1, category)
    addPlayer(players, newPlayer2, category)
    rankingId = rankMapDouble.get(str(team["poidsEquipe"]))
    fftId = team["inscriptionId"]
    newTeam = Team(fftId, newPlayer1.fftId, newPlayer2.fftId, rankingId)
    teams.append(newTeam)

def addPlayer(players, newPlayer, category):
    for player in players:
        if newPlayer.fftId == player.fftId:
            if player.rankingId != newPlayer.rankingId:
                player.rankingId = newPlayer.rankingId
            player.categories.append(category)
            updatePlayerBalance(player, category.amount)
            return
    newPlayer.categories.append(category)
    updatePlayerBalance(newPlayer, category.amount)
    players.append(newPlayer)

def updatePlayerBalance(player, amount):
    if not player.balance :
        player.balance = PlayerBalance.fromPlayer(player, amount)
        return
    if amount == 0 :
        return
    player.balance.remainingAmount += amount
    player.balance.finalAmount += amount
    player.balance.initialAmount += amount

def updateDBPlayers(players, sendNotif):
    playersMap = playerRepository.getPlayersMap()
    newPlayers = []
    messages = []
    newRankingsPlayers = []
    for player in players:
        playerInDB = playersMap.get(player.fftId)
        if playerInDB:
            checkCategories(player, playerInDB, sendNotif)
            if player.isDifferent(playerInDB):
                if playerInDB.rankingId != player.rankingId:
                    newRankingsPlayers.append((player, playerInDB.rankingId))
                player.id = playerInDB.id
                playerRepository.updatePlayer(playerInDB.id, player)
            playersMap.pop(player.fftId)
        else:
            newPlayers.append(player)
    for player in playersMap.values():
        deletePlayer(messages, player)
    sendMessages(newPlayers, newRankingsPlayers)
    if newPlayers :
        playerRepository.addPlayers(newPlayers)
    if messages :
        messageRepository.addMessages(messages)

def createPlayer(player):
    return {
        'id' : player.id,
        'fullName' : player.getFullName(),
        'ranking' : player.ranking.simple if player.ranking else None,
        'club' : player.club,
        'categories' : player.categories
    }

def deletePlayer(messages, player):
    if(playerRepository.deletePlayer(player)):
        msg = f"Désinscription de {player.getFullName()} ({player.club})"
        if player.ranking :
            msg += f" classé(e) {player.ranking.simple}"
        messages.append(Message("G", msg))
        for category in player.categories:
            messages.append(Message(category.code, msg))
    else:
        player.toDelete = True
        playerRepository.updatePlayer(player.id, player)
        msg = f"Tentative de suppression de {player.getFullName()} ({player.club})"
        if player.ranking :
            msg += f" classé(e) {player.ranking.simple}"
        msg += " échouée"
        messages.append(Message("ERROR", msg))

def updateDBTeams(teams):
    playersMap = playerRepository.getPlayersIdMap()
    teamsMap = teamRepository.getTeamsMap()
    newTeams = []
    for team in teams:
        teamInDB = teamsMap.get(team.fftId)
        if teamInDB:
            teamsMap.pop(teamInDB.fftId)
        else:
            team.player1Id = playersMap[team.player1Id]
            team.player2Id = playersMap[team.player2Id]
            newTeams.append(team)
    if newTeams:
        teamRepository.addTeams(newTeams)
    if teamsMap:
        teamRepository.deleteTeams([team.id for team in teamsMap.values()])

def checkCategories(player, playerInDB, sendNotif):
    newCategories = player.categories
    oldCategories = playerInDB.categories
    messages = []
    handleNewCategories(player, playerInDB, newCategories, oldCategories, messages, sendNotif)
    handleOldCategories(player, newCategories, oldCategories, messages, sendNotif)
    if len(messages) > 0 :
        playerBalanceRepository.updatePlayerBalanceByPlayerId(playerInDB.id, player.balance)
        if sendNotif:
            messageRepository.addMessages(messages)

def handleNewCategories(player, playerInDB, newCategories, oldCategories, messages, sendNotif):
    playerCategoriesToAdd = []
    for category in newCategories:
        if category not in oldCategories:
            playerCategory = PlayerCategories(playerInDB.id, category.id)
            playerCategoriesToAdd.append(playerCategory)
            if sendNotif:
                msg = f"Nouvelle inscription : {player.getFullName()} ({player.club})"
                if player.ranking :
                    msg += f" classé(e) {player.ranking.simple}"
                messages.append(Message(category.code, msg))
    if playerCategoriesToAdd:
        playerCategoriesRepository.addPlayerCategories(playerCategoriesToAdd)

def handleOldCategories(player, newCategories, oldCategories, messages, sendNotif):
    for category in oldCategories:
        if category not in newCategories:
            playerCategoriesRepository.deletePlayerCategoryByPlayerIdAndCategoryId(player.id, category.id)
            if sendNotif:
                msg = f"Désinscription de {player.getFullName()} ({player.club})"
                if player.ranking :
                    msg += f" classé(e) {player.ranking.simple}"
                messages.append(Message(category.code, msg))

def sendMessages(newPlayers, newRankingsPlayers):
    messages = []
    for player in newPlayers:
        msg = f"Nouvelle inscription : {player.getFullName()} ({player.club})"
        if player.ranking :
            msg += f" classé(e) {player.ranking.simple}"
        messages.append(Message("G", msg))
        for category in player.categories:
            messages.append(Message(category.code, msg))
    for player, rankingId in newRankingsPlayers:
        ranking = rankingRepository.getRankingById(rankingId)
        if ranking == player.ranking:
            continue
        msg = f"Reclassement de {player.getFullName()} ({ranking.simple} => {player.ranking.simple})"
        messages.append(Message("G", msg))
    messageRepository.addMessages(messages)