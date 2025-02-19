import discord.discordBusiness as discordBusiness
import batchs.batchs as batchs
import discord.discordNotif as discordNotif

from logger.logger import log, BATCH

async def pgwLoop(bot):
    log.info(BATCH, "Lancement du batch pgw")
    await discordBusiness.pgw(bot)

async def inscriptionsLoop():
    log.info(BATCH, "Lancement du batch inscriptions")
    await batchs.inscriptions()

async def sendNotifLoop(bot):
    log.info(BATCH, "Lancement du batch sendNotif")
    await discordNotif.sendNotif(bot)

async def updateMatchLoop():
    log.info(BATCH, "Lancement du batch updateMatch")
    await batchs.updateMatch()

async def updateCalLoop():
    log.info(BATCH, "Lancement du batch updateCal")
    await batchs.updateCalendar()