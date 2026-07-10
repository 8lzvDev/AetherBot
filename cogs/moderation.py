import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.LOG_CHANNEL_ID = 000000000000000000 # Mantenha seu ID aqui

    async def send_log(self, ctx, embed):
        channel = self.bot.get_channel(self.LOG_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)

    @commands.command(name="mutecall")
    async def mutecall(self, ctx, member: discord.Member, *, reason: str = "Não especificado"):
        await member.edit(mute=True)
        embed = discord.Embed(description=f"🔇 **{member.display_name}** foi silenciado na call.", color=0x2b2d31)
        embed.add_field(name="Motivo:", value=reason, inline=False)
        embed.set_author(name="Sistema de Moderação", icon_url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Moderador: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)
        await self.send_log(ctx, embed)

    @commands.command(name="unmutecall")
    async def unmutecall(self, ctx, member: discord.Member, *, reason: str = "Não especificado"):
        await member.edit(mute=False)
        embed = discord.Embed(description=f"🔊 **{member.display_name}** foi liberado na call.", color=0x2b2d31)
        embed.add_field(name="Motivo:", value=reason, inline=False)
        embed.set_author(name="Sistema de Moderação", icon_url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Moderador: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)
        await self.send_log(ctx, embed)

    @commands.command(name="lock")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(description="🔒 **Este canal foi trancado.**", color=0x2b2d31)
        embed.set_author(name="Sistema de Moderação", icon_url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Moderador: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)
        await self.send_log(ctx, embed)

    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = discord.Embed(description="🔓 **Este canal foi destrancado.**", color=0x2b2d31)
        embed.set_author(name="Sistema de Moderação", icon_url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Moderador: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)
        await self.send_log(ctx, embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
