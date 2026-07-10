import discord
from discord.ext import commands
from datetime import datetime

class TicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Abrir Ticket", style=discord.ButtonStyle.primary, custom_id="open_ticket_btn", emoji="📩")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⌛ Criando seu canal de suporte privado...", ephemeral=True)

class TicketPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="enviar_painel")
    @commands.has_permissions(administrator=True)
    async def enviar_painel(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass

        embed = discord.Embed(
            title="🎫 Central de Atendimento - AetherBot",
            description=(
                "Precisa de ajuda, suporte ou quer fazer uma denúncia?\n\n"
                "**Como proceder:**\n"
                "1️⃣ Clique no botão `Abrir Ticket` abaixo.\n"
                "2️⃣ Um canal privado será criado para você.\n"
                "3️⃣ Nossa equipe de staff estará pronta para te ajudar.\n\n"
                "*Evite abrir tickets sem necessidade para não sobrecarregar o suporte.*"
            ),
            color=discord.Color.from_rgb(114, 137, 218),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="AetherBot • Sistema de Gestão")

        await ctx.send(embed=embed, view=TicketButton())

async def setup(bot):
    await bot.add_cog(TicketPanel(bot))
