# Global packages
import sys
sys.path.append("modules")
from config import Config
from discord import Intents
from discord.ext import commands

DISCORD_GUILD_ID = int(Config.DISCORD_GUILD_ID)

intent = Intents(messages=True, members=True, guilds=True, reactions=True, message_content=True)
bot = commands.Bot(command_prefix='$', description='Tennis 2025', intents=intent)

@bot.command()
async def check(ctx):
    if ctx.message.guild.id != DISCORD_GUILD_ID: return
    await ctx.send("Connected !")

@bot.event
async def on_ready():
    print("Bot running...")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

def main():
    bot.run(Config.DISCORD_TOKEN)