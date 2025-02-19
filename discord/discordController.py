from config import Config
from discord import Intents
from discord.ext import commands
import discord.discordBusiness as discordBusiness
import batchs.batchsLauncher as batchsLauncher

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from logger.logger import log, BOT

scheduler = AsyncIOScheduler()

DISCORD_GUILD_ID = int(Config.DISCORD_GUILD_ID)

intent = Intents(messages=True, members=True, guilds=True, reactions=True, message_content=True)
bot = commands.Bot(command_prefix='$', description='Tennis 2025', intents=intent)

@bot.command()
async def check(ctx):
    await discordBusiness.check(ctx)

@bot.command()
async def nb(ctx):
    await discordBusiness.nb(bot, ctx)

@bot.command()
async def info(ctx, name = None):
    await discordBusiness.info(ctx, name)

@bot.command()
async def infos(ctx, name = None):
    await discordBusiness.info(ctx, name)

@bot.command()
async def pgw(ctx):
    await discordBusiness.pgw(bot)

@bot.command()
async def updateCourts(ctx):
    await discordBusiness.updateCourts(ctx)

@bot.command()
async def updateCategories(ctx):
    await discordBusiness.updateCategories(ctx)

@bot.command()
async def updateGrids(ctx):
    await discordBusiness.updateGrids(ctx)

@bot.command()
async def updateRankings(ctx):
    await discordBusiness.updateRankings(ctx)

@bot.command()
async def updateHomologation(ctx):
    await discordBusiness.updateHomologation(ctx)

@bot.command()
async def cmd(ctx):
    await discordBusiness.cmd(ctx)

@bot.command()
async def clear(ctx, nombre: int = 100):
    await discordBusiness.clear(ctx, nombre)

@bot.event
async def on_ready():
    log.info(BOT, "Connected !")
    scheduler.add_job(batchsLauncher.pgwLoop, CronTrigger(hour=7, minute=58, timezone=timezone('Europe/Paris')), args=[bot])
    scheduler.add_job(batchsLauncher.inscriptionsLoop, CronTrigger(second=30, timezone=timezone('Europe/Paris')))
    scheduler.add_job(batchsLauncher.sendNotifLoop, CronTrigger(second=0, timezone=timezone('Europe/Paris')), args=[bot])
    scheduler.add_job(batchsLauncher.updateMatchLoop, CronTrigger(hour=2, timezone=timezone('Europe/Paris')))
    scheduler.add_job(batchsLauncher.updateCalLoop, CronTrigger(hour=3, timezone=timezone('Europe/Paris')))
    scheduler.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.guild.id != DISCORD_GUILD_ID: 
        return
    await bot.process_commands(message)

def main():
    bot.run(Config.DISCORD_TOKEN)