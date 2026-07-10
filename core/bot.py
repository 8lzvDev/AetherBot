import discord
from discord.ext import commands
from core.config import Config
from core.logger import logger

class ProfessionalBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        
        super().__init__(
            command_prefix=Config.PREFIX,
            intents=intents,
            application_id=Config.APPLICATION_ID
        )

    async def setup_hook(self):
        logger.info("Carregando módulos (Cogs)...")
        
        # Lista de cogs planejados na estrutura do projeto
        initial_extensions = [
            "cogs.tickets",
            "cogs.moderation",
            "cogs.economy",
            "cogs.leveling",
            "cogs.automod",
            "cogs.logs",
            "cogs.welcome",
            "cogs.giveaways",
            "cogs.roles"
        ]
        
        for ext in initial_extensions:
            try:
                await self.load_extension(ext)
                logger.info(f"Módulo carregado: {ext}")
            except Exception as e:
                # Usamos warning ou error em vez de quebrar o bot inteiro se um cog falhar
                logger.warning(f"Não foi possível carregar {ext}: {e}")

    async def on_ready(self):
        logger.success(f"AetherBot está ONLINE! Conectado como {self.user} (ID: {self.user.id})")
