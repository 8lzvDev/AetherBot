import discord
from discord.ext import commands
from datetime import datetime
from core.logger import logger

class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Denúncia", 
                description="Criar Ticket de Denúncia", 
                emoji="🚨", 
                value="denuncia"
            ),
            discord.SelectOption(
                label="Dúvida", 
                description="Tirar uma Dúvida", 
                emoji="💬", 
                value="duvida"
            )
        ]
        super().__init__(placeholder="Selecione uma opção...", min_values=1, max_values=1, options=options, custom_id="ticket_select_menu")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        escolha = self.values[0].capitalize()
        
        channel_name = f"🎫-{self.values[0]}-{user.name.lower()}"
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        
        if existing_channel:
            await interaction.response.send_message(f"❌ Você já possui um ticket de {escolha} ativo em {existing_channel.mention}!", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        ticket_channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)
        
        embed_internal = discord.Embed(
            title=f"✨ Atendimento — {escolha}",
            description=(
                f"Olá {user.mention}, obrigado por entrar em contato.\n\n"
                "**┃ Próximos Passos**\n"
                f"• Explique detalhadamente o motivo da sua **{escolha}**.\n"
                "• Nossa equipe foi notificada e responderá o mais rápido possível.\n\n"
                "ℹ️ *Para fechar, use `!close`.*"
            ),
            color=discord.Color.from_str("#2b2d31")
        )
        
        await ticket_channel.send(content=f"{user.mention} ┃ {escolha}", embed=embed_internal)
        await interaction.response.send_message(f"✅ Seu ticket de {escolha} foi aberto em {ticket_channel.mention}", ephemeral=True)

class TicketSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setup_tickets")
    @commands.has_permissions(administrator=True)
    async def setup_tickets(self, ctx):
        """Gera o painel com menu de seleção com o nome correto da loja."""
        try:
            await ctx.message.delete()
        except:
            pass

        embed = discord.Embed(
            title="ZERO STORE — Suporte & Denúncias",
            description=(
                "Para manter nossa comunidade segura, use este canal para expor qualquer "
                "comportamento inadequado ou sanar suas dúvidas. Estamos prontos para agir, especialmente "
                "quando nenhum moderador estiver online nos chats, cobrindo interações no "
                "servidor, fora dele ou via mensagens privadas.\n\n"
                "Fique tranquilo: ao abrir o seu atendimento, nossa equipe iniciará um canal privado "
                "com você. Seu relato será avaliado com total sigilo, atenção e segurança pela "
                "nossa equipe."
            ),
            color=discord.Color.from_str("#2b2d31")
        )
        
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)

        await ctx.send(embed=embed, view=TicketSelectView())

    @commands.command(name="close")
    async def close_ticket(self, ctx):
        """Fecha o canal de ticket."""
        if "denuncia-" in ctx.channel.name or "duvida-" in ctx.channel.name or "ticket-" in ctx.channel.name:
            await ctx.send("🔒 **Este atendimento será encerrado em 5 segundos...**")
            import asyncio
            await asyncio.sleep(5)
            await ctx.channel.delete()
        else:
            await ctx.send("❌ Este comando só pode ser utilizado dentro de um ticket ativo.")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
