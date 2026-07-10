import sys
from loguru import logger

# Configuração do formato do log
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# Remove o logger padrão e adiciona o customizado no terminal
logger.remove()
logger.add(sys.stderr, format=log_format, level="INFO")

# Salva os logs em um arquivo dentro da pasta do bot
logger.add("bot/logs/bot.log", rotation="10 MB", retention="5 days", format=log_format, level="DEBUG")
