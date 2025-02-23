import discord.discordBusiness as discordBusiness
import batchs.batchs as batchs
import discord.discordNotif as discordNotif

from logger.logger import log, BATCH

async def pgwLoop(bot):
    log.info(BATCH, "Lancement du batch pgw")
    await discordBusiness.pgw(bot)
    log.info(BATCH, "Fin du batch pgw")

async def inscriptionsLoop():
    log.info(BATCH, "Lancement du batch inscriptions")
    await batchs.inscriptions()
    log.info(BATCH, "Fin du batch inscriptions")

async def sendNotifLoop(bot):
    log.info(BATCH, "Lancement du batch sendNotif")
    await discordNotif.sendNotif(bot)
    log.info(BATCH, "Fin du batch sendNotif")

async def updateMatchLoop():
    log.info(BATCH, "Lancement du batch updateMatch")
    await batchs.updateMatch()
    log.info(BATCH, "Fin du batch updateMatch")

async def updateCalLoop():
    log.info(BATCH, "Lancement du batch updateCal")
    await batchs.updateCalendar()
    log.info(BATCH, "Fin du batch updateCal")