import discord.discordBusiness as discordBusiness
import batchs.batchs as batchs
import discord.discordNotif as discordNotif

from repositories.SettingRepository import SettingRepository

from logger.logger import log, BATCH

settingRepository = SettingRepository()

async def pgwLoop(bot):
    if settingRepository.getBatchsActive() == False: return
    log.info(BATCH, "Lancement du batch pgw")
    await discordBusiness.pgw(bot)
    log.info(BATCH, "Fin du batch pgw")

async def inscriptionsLoop():
    if settingRepository.getBatchsActive() == False: return
    log.info(BATCH, "Lancement du batch inscriptions")
    await batchs.inscriptions()
    log.info(BATCH, "Fin du batch inscriptions")

async def sendNotifLoop(bot):
    if settingRepository.getBatchsActive() == False: return
    log.info(BATCH, "Lancement du batch sendNotif")
    await discordNotif.sendNotif(bot)
    log.info(BATCH, "Fin du batch sendNotif")

async def updateMatchLoop():
    if settingRepository.getBatchsActive() == False: return
    log.info(BATCH, "Lancement du batch updateMatch")
    await batchs.updateMatch()
    log.info(BATCH, "Fin du batch updateMatch")

async def updateCalLoop():
    if settingRepository.getBatchsActive() == False: return
    log.info(BATCH, "Lancement du batch updateCal")
    await batchs.updateCalendar()
    log.info(BATCH, "Fin du batch updateCal")