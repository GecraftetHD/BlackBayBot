import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
import cryptic_sdk as cryptic
import bankdata as db
from discord.ext.commands import CheckFailure

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
cryptic_user = os.getenv('env_user')
cryptic_password = os.getenv('env_password')
cryptic_wallet = os.getenv('env_wallet_uuid')
cryptic_key = os.getenv('env_wallet_key')
print("--------------------------------------")
print("logged in at Cryptic with Credentials:")
# print("Username:", cryptic_user)
# print("Password:", cryptic_password)
print("--------------------------------------")

bot = commands.Bot(command_prefix='<', intents=discord.Intents.all())
bot.remove_command('help')

client = cryptic.Client('wss://ws.cryptic-game.net')
client.login(cryptic_user, cryptic_password)


@bot.event
async def on_ready():
    print(f"Logged in as Discorduser: {bot.user.name}")
    bot.loop.create_task(status_task())


@bot.event
async def on_raw_reaction_add(payload):
    channel_id = payload.channel_id
    message_id = payload.message_id
    user = payload.user_id
    member = payload.member
    emoji = payload.emoji

    if user == bot.user or not db.is_bankchannel(channel_id, message_id):
        return
    print("True")
    print(f"{payload.member}")
    channel = bot.get_channel(channel_id)
    message = channel.get_partial_message(message_id)
    await message.remove_reaction(emoji, member)
    print("Reaction removed!")
    #id = db.get_employee()

    category = discord.utils.get(channel.guild.categories, name="tickets")
    overwrites = {
        channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        channel.guild.me: discord.PermissionOverwrite(read_messages=True),
        #channel.guild.id: discord.PermissionOverwrite(read_message=True)
    }

    channel2 = await channel.guild.create_text_channel('secret', overwrites=overwrites, category=category)


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
    if ctx.author.id == 333934370857418752:
        wallet: cryptic.Wallet = client.getUser().getWallet(cryptic_wallet, cryptic_key)
        embed = discord.Embed(title="BlackBay | Crytic Bank",
                              description=f"Aktueller Kontostand: {wallet.amount}")
        await ctx.send(embed=embed)
    else:

        embed = discord.Embed(title="BlackBay | Cryptic Bank",
                              description="Dazu hast du keine Rechte!")
        await ctx.send(embed=embed)


@bot.command()
async def create_wallet(ctx: commands.Context):
    user_id = ctx.author.id

    category = discord.utils.get(ctx.guild.categories, name="tickets")
    ticketNumber = db.wallets.count_documents({})
    channel1 = ctx.channel.id
    channel = ctx.channel.id if ctx.channel.name.startswith("ticket-") else (
        await ctx.guild.create_text_channel(f'Ticket-{ticketNumber}', category=category)).id
    print("Channel:", channel, "User_ID:", user_id)
    await channel1.send("Herzlichen Glückwunsch zu deinem neuen Konto")


@bot.command()
async def init_bank(ctx):
    # Definiert die Embeds
    embed1 = discord.Embed(title="BlackBay | Cryptic Bank",
                           description="Reagiere mit einem Klick auf den Brief um dir ein neues Bankkonto zu erstellen")
    embed2 = discord.Embed(title="BlackBay | Cryptic Bank",
                           description="Bankchannel gesetzt und in die Datenbank eingetragen. Diese Nachricht kann gelöscht werden.")
    # Sendet das Info-Embed
    await ctx.send(embed=embed2)
    # Sendet das richtige Embed
    message = await ctx.send(embed=embed1)
    # Fügt den Brief hinzu
    await message.add_reaction('📩')
    start_bank_id = ctx.channel.id
    start_bank_message_id = message.id
    db.insert_bank_channel(start_bank_id, start_bank_message_id)


@bot.command()
@commands.has_permissions(administrator=True)
async def addrole(ctx, args):
    try:
        y = int(args)
        embed = discord.Embed(title="BlackBay | Cryptic Bank",
                              description=f"Rolle mit der ID {args} in die Datenbank hinzugefügt.")
        db.insert_employee(args)
        await ctx.send(embed=embed)

    except:
        embed = discord.Embed(title="BlackBay | Cryptic Bank",
                              description="Bitte geben sie eine gültige Mitarbeiterrollen-ID ein!")
        await ctx.send(embed=embed)


@addrole.error
async def addrole_error(error, ctx):
    if isinstance(error, CheckFailure):
        embed = discord.Embed(title="BlackBay | Cryptic Bank",
                              description="Dazu hast du keine Rechte. Anzeige ist raus!")
        await ctx.send(embed=embed)


bot.load_extension('cogs.help')
bot.load_extension('cogs.bank')
bot.run(TOKEN)
client.logout()
