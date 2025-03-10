
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

async def inscriptions():
    players, teams = getPlayersAndTeams()
    if players : updateDBPlayers(players)
    if teams : updateDBTeams(teams)

async def updateMatch():
    return None

async def updateCalendar():
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
    newPlayer = Player.fromFFT(player)
    newPlayer.ranking = rankingRepository.getRankingBySimple(player['classementJoueur1'])
    newPlayer.rankingId = newPlayer.ranking.id
    addPlayer(players, newPlayer, category)

def addPlayersAndTeamInLists(players, teams, player, category):
    newPlayer1 = Player.fromFFT(player)
    newPlayer2 = Player.fromFFT2(player)
    newPlayer1.ranking = rankingRepository.getRankingBySimple(player['classementJoueur1'])
    newPlayer2.ranking = rankingRepository.getRankingBySimple(player['classementJoueur2'])
    addPlayer(players, newPlayer1, category)
    addPlayer(players, newPlayer2, category)
    ranking = None#TODO : team ranking
    fftId = player["inscriptionId"] #TODO : Check inscirptionId pour les players.team (conflit)
    newTeam = Team(fftId, newPlayer1, newPlayer2, ranking, 1)
    teams.append(newTeam)

def addPlayer(players, newPlayer, category):
    newPlayer.categories.append(category)
    updatePlayerBalance(newPlayer, category.amount)
    for player in players:
        if newPlayer.fftId == player.fftId : 
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

def updateDBPlayers(players):
    playersIdToDelete = playerRepository.getAllPlayersId()
    newPlayers = []
    oldPlayers = []
    newRankingsPlayers = []
    for player in players:
        playerInDB = playerRepository.getPlayerByFftId(player.fftId)
        if playerInDB:
            checkCategories(player, playerInDB)
            if player.isDifferent(playerInDB):
                if playerInDB.rankingId != player.rankingId:
                    print(playerInDB.rankingId)
                    newRankingsPlayers.append((player, playerInDB.rankingId))
                player.id = playerInDB.id
                playerRepository.updatePlayer(playerInDB.id, player)
            playersIdToDelete.remove(playerInDB.id)
        else:
            newPlayers.append(player)
    for playerId in playersIdToDelete:
        oldPlayers.append(createPlayer(playerRepository.getPlayerById(playerId)))
    sendNotif(newPlayers, oldPlayers, newRankingsPlayers)
    playerRepository.addPlayers(newPlayers)
    playerRepository.deletePlayers(playersIdToDelete)

def createPlayer(player):
    return {
        'fullName' : player.getFullName(),
        'ranking' : player.ranking.simple if player.ranking else None,
        'club' : player.club,
        'categories' : player.categories
    }

def updateDBTeams(teams):
    teamRepository.setTeamsToInactive()
    activeTeamsId = []
    for team in teams:
        teamInDB = teamRepository.getTeamByFftId(team.fftId)
        if teamInDB:
            activeTeamsId.append(teamInDB.id)
        else:
            team = teamRepository.addTeam(team)
            activeTeamsId.append(team.id)
    teamRepository.setTeamsToActive(activeTeamsId)
    teamRepository.deleteInactiveTeams()

def checkCategories(player, playerInDB):
    newCategories = player.categories
    oldCategories = playerInDB.categories
    messages = []
    for category in newCategories:
        if category not in oldCategories:
            playerCategory = PlayerCategories(playerInDB.id, category.id)
            PlayerCategoriesRepository.addPlayerCategory(playerCategory)
            msg = f"Nouvelle inscription : {player.getFullName()} ({player.club})"
            if player.ranking : msg += f" classé(e) {player.ranking.simple}"
            messages.append(Message(category.code, msg))

    for category in oldCategories:
        if category not in newCategories:
            playerCategory = playerCategoriesRepository.deletePlayerCategoryByPlayerIdAndCategoryId(player.id, category.id)
            msg = f"Désinscription de {player.getFullName()} ({player.club})"
            if player.ranking : msg += f" classé(e) {player.ranking.simple}"
            messages.append(Message(category.code, msg))
    if len(messages) > 0 :
        playerBalanceRepository.updatePlayerBalanceByPlayerId(playerInDB.id, player.balance)
        messageRepository.addMessages(messages)

def sendNotif(newPlayers, oldPlayers, newRankingsPlayers):
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
        print(rankingId)
        ranking = rankingRepository.getRankingById(rankingId)
        msg = f"Reclassement de {player.getFullName()} ({ranking.simple} => {player.ranking.simple})"
        messages.append(Message("G", msg))
    messageRepository.addMessages(messages)