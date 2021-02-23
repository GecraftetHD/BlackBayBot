import discord
from discord.ext import commands


class bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="bank", invoke_without_command=True)
    async def bank(self, ctx):
        embed = discord.Embed(title="BlackBay | Cryptic Bank",
                              description="Nutze <help <command> um dir genauere Infos zu einem Befehl anzeige zu lassen.",
                              colour=0x8080ff)
        embed.add_field(name="Adminstuff", value="`get_money` `add_transaction` `Platzhalter`")
        embed.add_field(name="Kontoverwaltung", value="`withdraw` `send` `history`")



        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(bank(bot))