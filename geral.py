# geral
import discord
from discord.ext import commands


class Geral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="listarcomandos")
    async def listar_comandos(self, ctx):
        comandos = [
            ("registro", "Registre-se no sistema"),
            ("listar_registros", "Lista registros (admins)"),
            ("demitir", "Demitir membro (admins)"),
            ("ticket", "Abrir ticket"),
            ("farm", "Painel de farm, venda, sujo"),
            ("verfarm", "Ver farms dos membros"),
            ("financeiro", "Painel financeiro"),
            ("saldo", "Ver saldo da facção"),
            ("addparceiro", "Adicionar parceiro (admins)"),
            ("parcerias", "Ver parcerias"),
            ("comissao", "Ver comissões de vendas")
        ]

        embed = discord.Embed(title="📜 Comandos Disponíveis", color=discord.Color.blue())
        for cmd, desc in comandos:
            embed.add_field(name=f"!{cmd}", value=desc, inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Geral(bot))
