import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
import cryptic_sdk as cryptic
import bankdata as db
from discord.ext.commands import CheckFailure
from discord.utils import get
from discord import Member, TextChannel
import config
import random
import string


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
cryptic_user = os.getenv('env_user')
cryptic_password = os.getenv('env_password')
cryptic_wallet = os.getenv('env_wallet_uuid')
cryptic_key = os.getenv('env_wallet_key')
cryptic_mod = os.getenv('env_mod')
bot_owner_id = os.getenv('bot_owner_id')
print("--------------------------------------")
print("logged in at Cryptic with Credentials:")
# print("Username:", cryptic_user)
# print("Password:", cryptic_password)
print("--------------------------------------")

bot = commands.Bot(command_prefix='<', intents=discord.Intents.all())
bot.remove_command('help')
def login():
    client = cryptic.Client('wss://ws.cryptic-game.net')
    client.login(cryptic_user, cryptic_password)


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    #print("Random string of length", length, "is:", result_str)
    return result_str



@bot.event
async def on_ready():
    print(f"Logged in as Discorduser: {bot.user.name}")
    bot.loop.create_task(status_task())


@bot.event
async def on_raw_reaction_add(payload):
    channel_id = payload.channel_id
    message_id = payload.message_id
    user = payload.user_id
    member: Member = payload.member
    emoji = payload.emoji

    if bot.user.id == int(user):
        return
    if not db.is_bankchannel(channel_id, message_id):
        return

    channel = bot.get_channel(channel_id)
    message = channel.get_partial_message(message_id)
    await message.remove_reaction(emoji, member)
    category = discord.utils.get(channel.guild.categories, name="tickets")
    overwrites = {
        channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        channel.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True,
                                                      embed_links=True, attach_files=True),
        get(channel.guild.roles, id=int(cryptic_mod)): discord.PermissionOverwrite(read_messages=True,
                                                                                   send_messages=True,
                                                                                   add_reactions=True, embed_links=True,
                                                                                   attach_files=True),
        member: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True,
                                            embed_links=True, attach_files=True)
    }

    ticketNumber = db.wallets.count_documents({})

    channel = await category.create_text_channel(name=f'ticket-{ticketNumber}', overwrites=overwrites)
    db.insert_wallet(channel.id, member.id, member, channel.name)
    embed = discord.Embed(title="BlackBay | Cryptic Bank",
                          description=f"Herzlichen Glückwunsch. Sie haben nun ihr Konto erstellt. {member.mention}")
    await channel.send(embed=embed)


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
    if ctx.author.id == bot_owner_id:
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
    await ctx.send(embed=embed2, delete_after=10)
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
        # db.insert_employee(args)
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


@bot.command()
@commands.has_permissions(administrator=True)
async def close_wallet(ctx):
    embed = discord.Embed(title="BlackBay | Cryptic Bank", description="Ticket wird in 20 Sekunden geschlossen!")
    embed.add_field(name="Abbrechen:", value="Gib `stop` ein um dies abzubrechen!")
    embed.set_footer(text="BlackBayBot")
    channel: TextChannel = ctx.channel
    await ctx.send(embed=embed)
    try:
        answ = await bot.wait_for("message", timeout=20)
        if answ.content == "stop":
            embed = discord.Embed(name="BlackBay | Cryptic Bank", description="Kontoschließung wurde abgebrochen...")
            await ctx.send(embed=embed)
        else:
            return

    except asyncio.TimeoutError:
        print("Timeout")

        db.close_status(ctx.channel.id)
        member_id = db.get_member_id_by_wallet_channel(channel.id)
        member = await ctx.guild.fetch_member(member_id)
        await channel.set_permissions(member, read_messages=False, send_messages=False, add_reactions=True,
                                            embed_links=False, attach_files=False)
        embed = discord.Embed(title="BlackBay | Cryptic Bank", description="Ticketstatus wurde auf `closed` gesetzt.")
        await ctx.send(embed=embed)


@bot.command()
async def pay_out(ctx):
    embed = discord.Embed(title="BlackBay | Cryptic Bank",
                          description="Ihr Geld wurden an 'b48bd270-e2a3-43a1-9ae9-a3dbb14257de' ausgezahlt")
    await ctx.send(embed=embed)


@bot.command()
async def deposit(ctx):
    code = "ch1cka1l9yv0wa"
    channel_id = ctx.channel.id
    db.is_wallet(channel_id)
    if not True:
        return
    embed = discord.Embed(title="BlackBay | Cryptic Bank",
                          description="Um einzahlen zu können, sende dein Geld bitte an untenstehende "
                                      "Zieladresse. Bitte nutze als Usage den unten angegeben Code, damit wir dir das Geld zuordnen können. Dieser Code wird jedes mal neugeneriert und verfällt nach einer Minute.")
    embed.add_field(name="Ziel-UUD", value="`8c9718e5-eceb-4d0d-a8dd-971e520e80b9 af8d6ce6c3`")
    code = get_random_string(10)
    embed.add_field(name="Code:", value=f"`{code}`")
    await ctx.send(embed=embed)

@bot.command()
async def withdraw(ctx):
    embed = discord.Embed(title="BlackBay | Cryptic Bank", description="Basic withdraw Embed")
    await ctx.send(embed=embed)


bot.load_extension('cogs.help')
bot.load_extension('cogs.bank')
bot.run(TOKEN)
#client.logout()
