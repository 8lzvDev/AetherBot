import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_custom(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass

        embed = discord.Embed(
            title="Lista de comandos",
            description=(
                "O comando **menu** na categoria principal, armazena vários "
                "sistemas e configurações da Nix! Com ele, você irá conseguir "
                "configurar a maior parte dos comandos e também personalizar seu bot!\n\n"
                
                "• **Principal**\n"
                "`blacklist`, `cupom`, `farmcall`, `gravar`, `menu`, `menu2`, `perm`, `registrador`, `registros`, `resetregistro`, `restcall`, `sairfamilia`, `setfamilia`, `usersite`\n\n"
                
                "• **Administração**\n"
                "`atself`, `bolao`, `bot-call`, `bots`, `cargo-react`, `container`, `drop`, `embed`, `embeds`, `formulario`, `listarbolao`, `pag`\n\n"
                
                "• **Moderação**\n"
                "`addcargo`, `addemoji`, `addpontos`, `addsaldo`, `addsticker`, `adms`, `adv`, `advrm`, `aviso`, `ban`, `bantempo`, `cargo`, `cargocall`, `cargotemp`, `castigo`, `chkcheat`, `clear`, `codigo`, `daily`, `deletemoji`, `groles`, `hierarquia`, `influencer`, `insta`, `kick`, `lavisos`, `lock`, `membros`, `mutecall`, `mutechat`, `nukechat`, `panela`, `pontos`, `premiar`, `prisao`, `registrar`, `removecargo`, `removepontos`, `removercastigo`, `reroll`, `removecargotemp`, `rmprisao`, `rmsaldo`, `roleall`, `say`, `staffpontos`, `streamer`, `unban`, `unbanall`, `unlock`, `unmute`, `unroleall`\n\n"
                
                "• **Usuário**\n"
                "`afk`, `ajuda`, `avatar`, `banner`, `carteira`, `configmed`, `divorce`, `gifts`, `invitediv`, `marry`, `player`, `postador`"
            ),
            color=discord.Color.from_str("#2b2d31")
        )
        
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
