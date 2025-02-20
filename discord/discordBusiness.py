import discord.discordFunctions as functions
from constants import constants
import moja.mojaService as mojaService

from repositories.ChannelRepository import ChannelRepository
from repositories.CategoryRepository import CategoryRepository
from repositories.MatchRepository import MatchRepository

channelRepository = ChannelRepository()
categoryRepository = CategoryRepository()
matchRepository = MatchRepository()

async def check(ctx):
    await ctx.send("Connected !")

async def nb(bot, ctx):
    category = channelRepository.getCategoryByChannelId(ctx.channel.id)
    if category is None :
        message = functions.getNbMessage()
        await ctx.send(message)
    else:
        await ctx.send(functions.getNbMessageByCategory(category))
    details = await functions.yesOrNo(bot, ctx, constants.ASK_DETAILS)
    if details :
        if category is None:
            await ctx.send(embed=functions.getPlayersDetails())
        else:
            await ctx.send(embed=functions.getPlayersDetailsByCategory(category))

async def info(ctx, matchLabel: str = None):
    if matchLabel == None:
        await ctx.send(constants.INFO_UNVALID_PARAM)
        return
    matchLabel = matchLabel.upper()
    match = matchRepository.getMatchByLabel(matchLabel)
    if match == None:
        await ctx.send(constants.NO_MATCH.replace("MATCH_LABEL", matchLabel))
        return
    message = functions.generateMatchInfosMessage(match)
    await ctx.send(message)

async def pgw(bot):
    channelId = channelRepository.getLogChannelId("WA")
    channel = await bot.fetch_channel(channelId)
    matches = False
    date = functions.getCurrentDate().strftime("%d/%m")
    requestDate = functions.getCurrentDate().strftime("%Y-%m-%d")
    matches = matchRepository.getMatchesForPlanning(requestDate)
    if matches == None or matches == []:
        await channel.send(constants.NO_PG.replace("DATE", date))
        return
    message = constants.PG.replace("DATE", date)
    for match in matches:
        if match.double :
            message += f"{match.hour} : {match.team1.getFullNameWithRanking()} contre {match.team2.getFullNameWithRanking()}\n"
        else:
            message += f"{match.hour} : {match.player1.getFullNameWithRanking()} contre {match.player2.getFullNameWithRanking()}\n"
    await channel.send(message)

async def updateCourts(ctx):
    response = mojaService.updateCourts()
    if response == 200 : await ctx.send("Courts mis à jour")
    elif response == 404 : await ctx.send("Homologation non trouvée")
    else : await ctx.send("Erreur lors de la mise à jour des courts")

async def updateCategories(ctx):
    response = mojaService.updateCategories()
    if response == 200 : await ctx.send("Categories mises à jour")
    else : await ctx.send("Erreur lors de la mise à jour des categories")

async def updateGrids(ctx):
    categories = categoryRepository.getAllCategories()
    for category in categories:
        response = mojaService.updateGrid(category.id, category.fftId)
        if response == 200 : await ctx.send("Découpages mise à jour pour l'épreuve " + category.code)
        elif response == 404 : await ctx.send("Epreuve non trouvée : " + category.code)
        else : await ctx.send("Erreur lors de la mise à jour des découpages de l'épreuve " + category.code)

async def updateRankings(ctx):
    response = mojaService.updateRankings()
    if response == 200 : await ctx.send("Classements mis à jour")
    else : await ctx.send("Erreur lors de la mise à jour des classements")

async def updateHomologation(ctx):
    response = mojaService.updateHomologation()
    if response == 200 : await ctx.send("Homologation mise à jour")
    else : await ctx.send("Erreur lors de la mise à jour de l'homologation")

async def updateMatches(ctx):
    response = mojaService.updateAllMatches()
    if response == 200 : await ctx.send("Matches mis à jour")
    else : await ctx.send("Erreur lors de la mise à jour des matches")

async def cmd(ctx):
    await ctx.send(constants.COMMANDS_LIST)

async def clear(ctx, nombre: int = 100):
    await ctx.channel.purge(limit=nombre+1, check=lambda msg: not msg.pinned)
