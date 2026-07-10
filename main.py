import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ... (seu código de load_extensions e outros eventos) ...

if __name__ == "__main__":
    bot.run(TOKEN)

@bot.check
async def verificar_servidor(ctx):
    with open("servidores_autorizados.txt", "r") as f:
        ids = f.read().splitlines()
    return str(ctx.guild.id) in ids
