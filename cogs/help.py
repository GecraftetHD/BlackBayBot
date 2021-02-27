import discord
from discord.ext import commands


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='help', invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Help",
                              icon_url="https://cdn.discordapp.com/avatars/804803893824585799/ce324bf84f155c482c69a398ccc18a9d.webp?size=1024",
                              description="Nutze <help <command> um dir genauere Infos zu einem Befehl anzeige zu lassen.",
                              colour=0x8080ff)

        embed.add_field(name="Fun <:thonkingbutcool:805521541562368080>", value="`get_money`")
        embed.add_field(name="Adminstuff <:Staff:807266444126453800>", value="`stop_pls` `init_bank` `close_wallet` `add_role` `get_money`")
        embed.add_field(name="misc <:PepeHappy:805521541688197171> ", value="`Info`")

        await ctx.send(embed=embed)





    @help.command()
    async def stop_pls(self, ctx):
        embed = discord.Embed(title="stop-command",
                              description="Stoppt den Bot. Hierfür werden spezialberechtigungen benötigt.",
                              colour=0x8080ff)
        embed.add_field(name="**Syntax**", value="<stop_pls")
        await ctx.send(embed=embed)


    @help.command()
    async def init_bank(self, ctx):
        embed = discord.Embed(title="BlackBay | Cryptic Bank",
                              description="Legt den Bank Kanal fest. Hierfür werden spezialberechtigungen benötigt.",
                              colour=0x8080ff)
        embed.add_field(name="**Syntax**", value="<init_bank")
        await ctx.send(embed=embed)

    @help.command()
    async def close_wallet(self, ctx):
        embed = discord.Embed(title="BlackBay | Cryptic Bank",
                              description="Schließt ein Wallet. Hierfür werden spezialberechtigungen benötigt.",
                              colour=0x8080ff)
        embed.add_field(name="**Syntax**", value="<close_wallet")
        await ctx.send(embed=embed)

    @help.command()
    async def add_role(self, ctx):
        embed = discord.Embed(title="BlackBay | Cryptic Bank",
                              description="Legt die Mitarbeiter Rolle fest. Hierfür werden spezialberechtigungen benötigt.",
                              colour=0x8080ff)
        embed.add_field(name="**Syntax**", value="<addrole <id")
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(help(bot))
