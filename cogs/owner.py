import discord
from discord.ext import commands
import sys

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown", aliases=["desligar"])
    async def shutdown(self, ctx):
        """Desliga o bot com segurança (Apenas o Criador)."""
        # Substitua o número abaixo pelo seu ID real do Discord se quiser travar só para você
        # Exemplo: if ctx.author.id != 1525015143593803928:
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("❌ Apenas administradores/criadores podem desligar o bot.")

        embed = discord.Embed(
            title="🔌 Desligando...",
            description=f"O bot está sendo encerrado por {ctx.author.mention}.",
            color=discord.Color.from_str("#2b2d31")
        )
        await ctx.send(embed=embed)
        await self.bot.close()
        sys.exit()

async def setup(bot):
    await bot.add_cog(Owner(bot))
