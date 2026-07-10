import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv("DISCORD_TOKEN")
    APPLICATION_ID = os.getenv("APPLICATION_ID")
    PREFIX = os.getenv("COMMAND_PREFIX", "!")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://db.sqlite3")
