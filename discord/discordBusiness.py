import discord.discordFunctions as functions
from constants import constants

from repositories.ChannelRepository import ChannelRepository
from repositories.CategoryRepository import CategoryRepository
from repositories.MatchRepository import MatchRepository

channelRepository = ChannelRepository()
categoryRepository = CategoryRepository()
matchsRepository = MatchRepository()

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
    match = matchsRepository.getMatchByLabel(matchLabel)
    if match == None:
        await ctx.send(constants.NO_MATCH.replace("MATCH_LABEL", matchLabel))
        return
    message = functions.generateMatchInfosMessage(match)
    await ctx.send(message)

async def pgw(bot):
    channelId = channelRepository.getLogChannelId("WA")
    channel = await bot.fetch_channel(channelId)
    matchs = False
    date = functions.getCurrentDate().strftime("%d/%m")
    requestDate = functions.getCurrentDate().strftime("%Y-%m-%d")
    matchs = matchsRepository.getMatchesForPlanning(requestDate)
    if matchs == None or matchs == []:
        await channel.send(constants.NO_PG.replace("DATE", date))
        return
    message = constants.PG.replace("DATE", date)
    for match in matchs:
        if match.double :
            message += f"{match.hour} : {match.team1.getFullNameWithRanking()} contre {match.team2.getFullNameWithRanking()}\n"
        else:
            message += f"{match.hour} : {match.player1.getFullNameWithRanking()} contre {match.player2.getFullNameWithRanking()}\n"
    await channel.send(message)

async def cmd(ctx):
    await ctx.send(constants.COMMANDS_LIST)

async def clear(ctx, nombre: int = 100):
    await ctx.channel.purge(limit=nombre+1, check=lambda msg: not msg.pinned)
