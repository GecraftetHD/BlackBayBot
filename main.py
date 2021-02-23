import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
import cryptic_sdk as cryptic
import bankdata as db



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
cryptic_user = os.getenv('env_user')
cryptic_password = os.getenv('env_password')
cryptic_wallet = os.getenv('env_wallet_uuid')
cryptic_key = os.getenv('env_wallet_key')
print("--------------------------------------")
print("logged in at Cryptic with Credentials:")
#print("Username:", cryptic_user)
#print("Password:", cryptic_password)
print("--------------------------------------")

bot = commands.Bot(command_prefix='<', intents=discord.Intents.all())
bot.remove_command('help')

client = cryptic.Client('wss://ws.cryptic-game.net')
client.login(cryptic_user, cryptic_password)


@bot.event
async def on_ready():
    print("Logged in as Discorduser: {}".format(bot.user.name))
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

    wallet: cryptic.Wallet = client.getUser().getWallet(cryptic_wallet, cryptic_key)
    await ctx.send(wallet.amount)



@bot.command()
async def create_wallet(ctx: commands.Context):
    user_id = ctx.author.id

    category = discord.utils.get(ctx.guild.categories, name="tickets")
    ticketNumber = db.wallets.count_documents({})
    channel = ctx.channel.id if ctx.channel.name.startswith("ticket-") else (await ctx.guild.create_text_channel(f'Ticket-{ticketNumber}', category=category)).id
    print("Channel:", channel, "User_ID:", user_id)




bot.load_extension('cogs.help')
bot.load_extension('cogs.bank')
bot.run(TOKEN)
client.logout()
