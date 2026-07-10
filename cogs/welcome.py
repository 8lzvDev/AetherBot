import discord
from discord.ext import commands
from core.logger import logger

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Procura um canal chamado 'boas-vindas' ou 'welcome' no servidor
        channel = discord.utils.get(member.guild.text_channels, name="boas-vindas") or \
                  discord.utils.get(member.guild.text_channels, name="welcome")
        
        if channel:
            embed = discord.Embed(
                title="👋 Bem-vindo(a)!",
                description=f"Olá {member.mention}, seja muito bem-vindo(a) ao **{member.guild.name}**!\n"
                            f"Atualmente somos **{member.guild.member_count}** membros.",
                color=discord.Color.purple()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"ID do usuário: {member.id}")
            
            await channel.send(embed=embed)
            logger.info(f"Mensagem de boas-vindas enviada para {member} no servidor {member.guild.name}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Procura um canal de saída ou logs para registrar a saída do membro
        channel = discord.utils.get(member.guild.text_channels, name="sair") or \
                  discord.utils.get(member.guild.text_channels, name="logs")
        
        if channel:
            embed = discord.Embed(
                title="🏃 Saiu do servidor",
                description=f"**{member.name}** pediu para sair. Que pena! 😢",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            
            await channel.send(embed=embed)
            logger.info(f"{member} saiu do servidor {member.guild.name}")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
