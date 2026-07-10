import discord
from discord.ext import commands
import os

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "palavras_proibidas.txt"
        self.banned_words = self.load_words()

    def load_words(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write("palavrao1\npalavrao2\n")
            return ["palavrao1", "palavrao2"]
        with open(self.file_path, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f.readlines() if line.strip()]

    def save_words(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            for word in self.banned_words:
                f.write(f"{word}\n")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.guild and message.author.guild_permissions.administrator:
            return
        message_content = message.content.lower()
        for word in self.banned_words:
            if word in message_content:
                try:
                    await message.delete()
                    warning = await message.channel.send(f"⚠️ **{message.author.mention}**, mensagem removida pelo AutoMod!")
                    await warning.delete(delay=5)
                except:
                    pass
                break

    @commands.command(name="add_palavra")
    @commands.has_permissions(administrator=True)
    async def add_palavra(self, ctx, *, palavra: str):
        palavra = palabra.lower().strip()
        if palavra in self.banned_words:
            await ctx.send("❌ Essa palavra já está no filtro!")
            return
        self.banned_words.append(palavra)
        self.save_words()
        await ctx.send(f"✅ Palavra `{palavra}` adicionada ao AutoMod!")

    @commands.command(name="lista_palavras")
    @commands.has_permissions(administrator=True)
    async def lista_palavras(self, ctx):
        if not self.banned_words:
            await ctx.send("📝 Lista vazia.")
            return
        await ctx.send(f"🛑 **Palavras Bloqueadas:** {', '.join(self.banned_words)}")

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
