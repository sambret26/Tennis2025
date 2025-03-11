from discord.ui import Button, View
from discord import Embed, ButtonStyle
from constants import constants
from datetime import datetime as date
from datetime import timedelta

from repositories.PlayerRepository import PlayerRepository
from repositories.CategoryRepository import CategoryRepository
from repositories.PlayerCategoriesRepository import PlayerCategoriesRepository
from repositories.RankingRepository import RankingRepository

categoryRepository = CategoryRepository()
playerRepository = PlayerRepository()
playerCategoriesRepository = PlayerCategoriesRepository()
rankingRepository = RankingRepository()

def getNbMessage():
    categories = categoryRepository.getAllCategories() #Improvement : Ne pas lire les catégories à chaque fois
    nb = playerRepository.getNumberPlayers()
    message = "Il y a {} inscrit{} dans le tournoi".format(nb, '' if nb <2 else 's')
    for category in categories :
        message += f"\n\t\t{getNbMessageByCategory(category)}"
    return message

def getNbMessageByCategory(category):
    nb = playerCategoriesRepository.getNumberPlayersByCategory(category.id)
    return "Il y a {} inscrit{} dans la catégorie {}".format(nb, '' if nb <2 else 's', category.code)

def getPlayersDetails():
    categories = categoryRepository.getAllCategories() #Improvement : Ne pas lire les catégories à chaque fois
    rankings = rankingRepository.getAllRankings() # Improvement : Ne pas lire les rankings à chaque fois
    embed = Embed(title = constants.NB_INSCRITS_BY_CAT, color = constants.EMBED_COLOR)
    playersRankingIds = playerRepository.getRankingIds()
    embed.add_field(name = constants.TOTAL, value = rankingMessage(rankings, playersRankingIds), inline = False)
    for category in categories:
        playersRankingIdsByCategories = playerRepository.getRankingIdsByCategoryId(category.id)
        embed.add_field(name = category.code, value = rankingMessage(rankings, playersRankingIdsByCategories), inline = False)
    return embed

def getPlayersDetailsByCategory(category):
    rankings = rankingRepository.getAllRankings() # Improvement : Ne pas lire les rankings à chaque fois
    embed = Embed(title = constants.NB_INSCRITS, color = constants.EMBED_COLOR)
    playersRankingIdsByCategories = playerRepository.getRankingIdsByCategoryId(category.id)
    embed.add_field(name = category.code, value = rankingMessage(rankings, playersRankingIdsByCategories), inline = False)
    return embed

def rankingMessage(rankings, playersRankingIds):
    message = ""
    for ranking in rankings:
        if ranking.id in playersRankingIds:
            message += f"{ranking.simple.ljust(4)} : {playersRankingIds.count(ranking.id)}\n"
    return message

def generateMatchInfosMessage(match):
    if match.finish : return generateMatchFinishInfosMessage(match)
    return generateMatchNotFinishInfosMessage(match)

def generateMatchFinishInfosMessage(match):
    entity1 = match.team1 if match.double else match.player1
    entity2 = match.team2 if match.double else match.player2
    info = f"Le match {match.label} a opposé {entity1.getFullName()} et {entity2.getFullName()}"
    if match.day : info += f" le {match.getFormattedDate()}"
    if match.hour : info += f" à {match.getFormattedHour()}"
    if match.court : info += f" sur le {match.court.name.lower()}"
    info += '.'
    if match.winner : 
        info += f" Le gagnant est {match.winner.getFullName()}"
        if match.score : info += f" ({match.score})"
        info += '.'
    if match.teamWinner :
        info += f" La paire gagnante est {match.teamWinner.getFullName()}"
        if match.score : info += f" ({match.score})"
        info += '.'
    return info

def generateMatchNotFinishInfosMessage(match):
    entity1 = match.team1 if match.double else match.player1
    entity2 = match.team2 if match.double else match.player2
    if entity1 and entity2 :
        info = f"Le match {match.label} opposera {entity1.getFullName()} à {entity2.getFullName()}"
    elif entity1 :
        info = f"Le match {match.label} opposera {entity1.getFullName()} à ?"
    elif entity2 :
        info = f"Le match {match.label} opposera {entity2.getFullName()} à ?"
    else :
        info = f"Le match {match.label} se jouera "
    if match.day : info += f" le {match.getFormattedDate()}"
    if match.hour : info += f" à {match.getFormattedHour()}"
    if match.court : info += f" sur le {match.court.name.lower()}"
    info += "."
    return info

def getCurrentDate():
    return date.now() + timedelta(hours=0)

async def yesOrNo(bot, ctx, message):
    return await question(bot, ctx, message, constants.YES_OR_NO)

async def question(bot, ctx, message, choices):
    while (len(choices) > 0):
        questionChoices = choices[:4]
        if(len(questionChoices) == 4):
            questionChoices.append(constants.QUESTION_MORE)
        result = await question5Max(bot, ctx, message, questionChoices)
        if result != "Next": return result
        choices = choices[4:]

async def question5Max(bot, ctx, message, choices):

    def check(i): return i.user.id == ctx.author.id and i.message.id == choice.id

    buttons = generateButtons(choices)
    view = View()
    for button in buttons : view.add_item(button)
    choice = await ctx.send(message, view=view)
    interaction = await bot.wait_for("interaction", check=check)
    custom_id = interaction.data['custom_id']
    await interaction.response.edit_message(content=f"{message} ({custom_id})")
    if custom_id.isdigit() : return int(custom_id)
    return custom_id

def generateButtons(choices):
    buttons = []
    for (index, choice) in enumerate(choices):
        button = Button(label=choice[0], custom_id=choice[1], style=findStyle(index, choice[2] if len(choice) >  2 else None))
        buttons.append(button)
    return buttons

def findStyle(index, value):
    if value != None and value.lower() == constants.GREEN: return ButtonStyle.green
    if value != None and value.lower() == constants.RED: return ButtonStyle.red
    if value != None and value.lower() == constants.BLUE: return ButtonStyle.blue
    if index % 3 == 0: return ButtonStyle.green
    if index % 3 == 1: return ButtonStyle.red
    return ButtonStyle.blue
