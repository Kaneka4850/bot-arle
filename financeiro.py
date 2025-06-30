import discord
from discord.ext import commands
from utils import carrega, salva

FINANCE_FILE = "financeiro.json"

Financeiro = carrega(FINANCE_FILE, {"entradas": [], "saidas": [], "gastos": []})


class FinanceiroCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def financeiro(self, ctx):
        view = discord.ui.View()

        async def abrir_modal(interaction: discord.Interaction):
            await interaction.response.send_modal(FinanceiroModal())

        botao = discord.ui.Button(label="Registrar Financeiro", style=discord.ButtonStyle.blurple)
        botao.callback = abrir_modal
        view.add_item(botao)

        await ctx.send("Clique para registrar no financeiro:", view=view)

    @commands.command(name="saldo")
    async def saldo(self, ctx):
        entradas = sum(Financeiro.get("entradas", []))
        saidas = sum(Financeiro.get("saidas", []))
        saldo_atual = entradas - saidas

        await ctx.send(
            f"💰 **Saldo atual:**\n"
            f"Entradas: R${entradas:.2f}\n"
            f"Saídas: R${saidas:.2f}\n"
            f"Saldo: R${saldo_atual:.2f} {'(positivo)' if saldo_atual >= 0 else '(negativo)'}"
        )


class FinanceiroModal(discord.ui.Modal, title="Registrar Financeiro"):
    tipo = discord.ui.TextInput(label="Tipo (entrada, saida, gasto)", max_length=10)
    valor = discord.ui.TextInput(label="Valor", max_length=15)

    async def on_submit(self, interaction: discord.Interaction):
        tipo = self.tipo.value.lower()
        try:
            valor = float(self.valor.value)
            if valor <= 0:
                raise ValueError
        except ValueError:
            return await interaction.response.send_message("❌ Valor inválido.", ephemeral=True)

        if tipo not in ["entrada", "saida", "gasto"]:
            return await interaction.response.send_message("❌ Tipo inválido.", ephemeral=True)

        Financeiro.setdefault(tipo + "s", []).append(valor)
        salva(FINANCE_FILE, Financeiro)

        await interaction.response.send_message(f"✅ {tipo.capitalize()} de R${valor} registrada.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(FinanceiroCog(bot))
