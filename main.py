import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
from cryptic_sdk import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
print(USERNAME, PASSWORD)

bot = commands.Bot(command_prefix='<', intents=discord.Intents.all())
bot.remove_command('help')


@bot.event
async def on_ready():
    print("Ich habe mich eingeloggt als User {}".format(bot.user.name))
    bot.loop.create_task(status_task())


async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game('BlackBay Bank Bot ;D'), status=discord.Status.online)
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game('BlackBay x Cryptic | cryptic-game.net'),
                                  status=discord.Status.online)
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game('<help | Blackbay.tk/bot'), status=discord.Status.online)
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game('mit euren Transaktionen.'), status=discord.Status.online)
        await asyncio.sleep(10)


@bot.command()
async def get_money(ctx):
    client = Client('wss://ws.cryptic-game.net')
    print(USERNAME, PASSWORD)
    client.login(USERNAME, PASSWORD)
    print(client.getUser().name)


bot.load_extension('cogs.help')
bot.run(TOKEN)
