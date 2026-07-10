import discord
from discord.ext import commands
import json
import os
import random
from datetime import datetime, timedelta

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "bot/data/economy.json"
        self.cooldown_file = "bot/data/cooldowns.json"
        self.ensure_files()

    def ensure_files(self):
        """Garante que as pastas e arquivos de dados existam."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump({}, f)
        if not os.path.exists(self.cooldown_file):
            with open(self.cooldown_file, "w") as f:
                json.dump({}, f)

    def load_json(self, file_path):
        with open(file_path, "r") as f:
            return json.load(f)

    def save_json(self, file_path, data):
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def get_balance(self, user_id):
        users = self.load_json(self.data_file)
        uid = str(user_id)
        if uid not in users:
            users[uid] = {"carteira": 0, "banco": 0}
            self.save_json(self.data_file, users)
        return users[uid]

    def update_balance(self, user_id, carteira_change=0, banco_change=0):
        users = self.load_json(self.data_file)
        uid = str(user_id)
        if uid not in users:
            users[uid] = {"carteira": 0, "banco": 0}
        
        users[uid]["carteira"] += carteira_change
        users[uid]["banco"] += banco_change
        self.save_json(self.data_file, users)

    def create_embed(self, ctx, title, description):
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.from_str("#2b2d31")
        )
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        return embed

    @commands.command(name="daily")
    async def daily(self, ctx):
        """Resgata a recompensa diária de moedas."""
        user_id = str(ctx.author.id)
        cooldowns = self.load_json(self.cooldown_file)
        now = datetime.utcnow()

        if user_id in cooldowns:
            last_daily = datetime.fromisoformat(cooldowns[user_id])
            if now < last_daily + timedelta(hours=24):
                remaining = (last_daily + timedelta(hours=24)) - now
                hours, remainder = divmod(int(remaining.total_seconds()), 3600)
                minutes, _ = divmod(remainder, 60)
                
                embed = self.create_embed(
                    ctx, 
                    "⏳ Cooldown", 
                    f"Você já coletou seu prêmio diário hoje!\nVolte em **{hours}h {minutes}m**."
                )
                return await ctx.send(embed=embed)

        # Recompensa aleatória entre 500 e 1500 moedas
        quantia = random.randint(500, 1500)
        self.update_balance(ctx.author.id, carteira_change=quantia)
        
        cooldowns[user_id] = now.isoformat()
        self.save_json(self.cooldown_file, cooldowns)

        embed = self.create_embed(
            ctx, 
            "💰 Recompensa Diária", 
            f"Parabéns {ctx.author.mention}! Você resgatou suas moedas diárias e ganhou **+${quantia}** na sua carteira."
        )
        await ctx.send(embed=embed)

    @commands.command(name="carteira", aliases=["atm", "saldo"])
    async def carteira(self, ctx, member: discord.Member = None):
        """Mostra o saldo da carteira e do banco."""
        target = member or ctx.author
        balance = self.get_balance(target.id)
        
        total = balance["carteira"] + balance["banco"]

        description = (
            f"Visualizando as finanças de {target.mention}:\n\n"
            f"💵 **Carteira:** `${balance['carteira']}`\n"
            f"🏦 **Banco:** `${balance['banco']}`\n\n"
            f"💳 **Total Geral:** `${total}`"
        )

        embed = self.create_embed(ctx, "💳 Saldo Bancário", description)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
