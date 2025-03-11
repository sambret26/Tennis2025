
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

import moja.mojaService as mojaService

playerRepository = PlayerRepository()
teamRepository = TeamRepository()
categoryRepository = CategoryRepository()
rankingRepository = RankingRepository()
messageRepository = MessageRepository()
playerBalanceRepository = PlayerBalanceRepository()
playerCategoriesRepository = PlayerCategoriesRepository()

def inscriptions(sendNotif):
    players, teams = getPlayersAndTeams()
    if players : updateDBPlayers(players, sendNotif)
    if teams : updateDBTeams(teams)

def updateMatch():
    return mojaService.updateAllMatches()

def updateCalendar():
    return None

def getPlayersAndTeams():
    players = []
    teams = []
    categories = categoryRepository.getAllCategories()
    for category in categories:
        datas = mojaService.getCategoryInfos(category.fftId)
        if not datas : return None, None
        for player in datas["listJoueurInscrit"]:
            if category.code.startswith("S"): addPlayerInPlayersList(players, player, category)
            else : addPlayersAndTeamInLists(players, teams, player, category)
    return players, teams

def addPlayerInPlayersList(players, player, category):
    #TODO RankingMap
    newPlayer = Player.fromFFT(player)
    newPlayer.ranking = rankingRepository.getRankingBySimple(player['classementJoueur1'])
    newPlayer.rankingId = newPlayer.ranking.id
    addPlayer(players, newPlayer, category)

def addPlayersAndTeamInLists(players, teams, team, category):
    #TODO RankingMap
    newPlayer1 = Player.fromFFT(team)
    newPlayer2 = Player.fromFFT2(team)
    newPlayer1.ranking = rankingRepository.getRankingBySimple(team['classementJoueur1'])
    newPlayer2.ranking = rankingRepository.getRankingBySimple(team['classementJoueur2'])
    addPlayer(players, newPlayer1, category)
    addPlayer(players, newPlayer2, category)
    ranking = rankingRepository.getRankingByDouble(str(team["poidsEquipe"])).id
    fftId = team["inscriptionId"]
    newTeam = Team(fftId, newPlayer1.fftId, newPlayer2.fftId, ranking)
    teams.append(newTeam)

def addPlayer(players, newPlayer, category):
    newPlayer.categories.append(category)
    updatePlayerBalance(newPlayer, category.amount)
    for player in players:
        if newPlayer.fftId == player.fftId : 
            player.categories.append(category)
            return
    players.append(newPlayer)

def updatePlayerBalance(player, amount):
    if not player.balance :
        player.balance = PlayerBalance.fromPlayer(player, amount)
        return
    if amount == 0 : return
    player.balance.remainingAmount += amount
    player.balance.finalAmount += amount
    player.balance.initialAmount += amount

def updateDBPlayers(players, sendNotif):
    playersIdToDelete = playerRepository.getAllPlayersId()
    newPlayers = []
    oldPlayers = []
    newRankingsPlayers = []
    for player in players:
        playerInDB = playerRepository.getPlayerByFftId(player.fftId)
        if playerInDB:
            checkCategories(player, playerInDB, sendNotif)
            if player.isDifferent(playerInDB):
                if playerInDB.rankingId != player.rankingId:
                    newRankingsPlayers.append((player, playerInDB.rankingId))
                player.id = playerInDB.id
                playerRepository.updatePlayer(playerInDB.id, player)
            playersIdToDelete.remove(playerInDB.id)
        else:
            newPlayers.append(player)
    for playerId in playersIdToDelete:
        oldPlayers.append(createPlayer(playerRepository.getPlayerById(playerId)))
    sendMessages(newPlayers, oldPlayers, newRankingsPlayers)
    if newPlayers != []: playerRepository.addPlayers(newPlayers)
    playerRepository.deletePlayers(playersIdToDelete)

def createPlayer(player):
    return {
        'fullName' : player.getFullName(),
        'ranking' : player.ranking.simple if player.ranking else None,
        'club' : player.club,
        'categories' : player.categories
    }

def updateDBTeams(teams):
    playersMap = playerRepository.getPlayersMap()
    teamsIdToDelete = teamRepository.getAllTeamsId()
    newTeams = []
    for team in teams:
        teamInDB = teamRepository.getTeamByFftId(team.fftId)
        if teamInDB:
            teamsIdToDelete.remove(teamInDB.id)
        else:
            team.player1Id = playersMap[team.player1Id]
            team.player2Id = playersMap[team.player2Id]
            newTeams.append(team)
    if newTeams != []: teamRepository.addTeams(newTeams)
    teamRepository.deleteTeams(teamsIdToDelete)

def checkCategories(player, playerInDB, sendNotif):
    newCategories = player.categories
    oldCategories = playerInDB.categories
    messages = []
    for category in newCategories:
        if category not in oldCategories:
            playerCategory = PlayerCategories(playerInDB.id, category.id)
            PlayerCategoriesRepository.addPlayerCategory(playerCategory)
            msg = f"Nouvelle inscription : {player.getFullName()} ({player.club})"
            if player.ranking : msg += f" classé(e) {player.ranking.simple}"
            if sendNotif : messages.append(Message(category.code, msg))

    for category in oldCategories:
        if category not in newCategories:
            playerCategory = playerCategoriesRepository.deletePlayerCategoryByPlayerIdAndCategoryId(player.id, category.id)
            msg = f"Désinscription de {player.getFullName()} ({player.club})"
            if player.ranking : msg += f" classé(e) {player.ranking.simple}"
            if sendNotif : messages.append(Message(category.code, msg))
    if sendNotif and len(messages) > 0 :
        playerBalanceRepository.updatePlayerBalanceByPlayerId(playerInDB.id, player.balance)
        messageRepository.addMessages(messages)

def sendMessages(newPlayers, oldPlayers, newRankingsPlayers):
    messages = []
    for player in newPlayers:
        msg = f"Nouvelle inscription : {player.getFullName()} ({player.club})"
        if player.ranking : msg += f" classé(e) {player.ranking.simple}"
        messages.append(Message("G", msg))
        for category in player.categories:
            messages.append(Message(category.code, msg))
    for player in oldPlayers:
        msg = f"Désinscription de {player["fullName"]} ({player["club"]})"
        if player["ranking"] : msg += f" classé(e) {player["ranking"]}"
        messages.append(Message("G", msg))
        for category in player["categories"]:
            messages.append(Message(category.code, msg))
    for player, rankingId in newRankingsPlayers:
        ranking = rankingRepository.getRankingById(rankingId)
        msg = f"Reclassement de {player.getFullName()} ({ranking.simple} => {player.ranking.simple})"
        messages.append(Message("G", msg))
    messageRepository.addMessages(messages)