# Farm
import discord
from discord.ext import commands
from utils import carrega, salva

FARMS_FILE = "farm.json"
FINANCE_FILE = "financeiro.json"

Farms = carrega(FARMS_FILE, {})
Financeiro = carrega(FINANCE_FILE, {"entradas": [], "saidas": [], "gastos": []})

chavinha = 630
nitrox = 60
suspensao = 60
disco = 150


class Farm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def farm(self, ctx):
        view = discord.ui.View()

        async def abrir_farm(interaction: discord.Interaction):
            await interaction.response.send_modal(FarmModal(ctx.author.id, ctx.author.name))

        async def abrir_venda(interaction: discord.Interaction):
            await interaction.response.send_modal(VendaModal(ctx.author.id, ctx.author.name))

        async def abrir_sujo(interaction: discord.Interaction):
            await interaction.response.send_modal(SujoModal(ctx.author.id, ctx.author.name))

        btn_farm = discord.ui.Button(label="Registrar Farm", style=discord.ButtonStyle.green)
        btn_venda = discord.ui.Button(label="Registrar Venda", style=discord.ButtonStyle.blurple)
        btn_sujo = discord.ui.Button(label="Dinheiro Sujo", style=discord.ButtonStyle.red)

        btn_farm.callback = abrir_farm
        btn_venda.callback = abrir_venda
        btn_sujo.callback = abrir_sujo

        view.add_item(btn_farm)
        view.add_item(btn_venda)
        view.add_item(btn_sujo)

        await ctx.send("Selecione o que deseja registrar:", view=view)

    @commands.command()
    async def verfarm(self, ctx):
        embed = discord.Embed(title="📊 Farm dos Membros", color=discord.Color.blue())

        for uid, user_data in Farms.items():
            usuario = user_data.get("usuario", "Desconhecido")

            farm_nitrox = user_data.get("nitrox", 0)
            farm_chavinha = user_data.get("chavinha", 0)
            farm_disco = user_data.get("disco", 0)
            farm_suspensao = user_data.get("suspensao", 0)

            atingiu_meta = (
                farm_nitrox >= nitrox and
                farm_chavinha >= chavinha and
                farm_disco >= disco and
                farm_suspensao >= suspensao
            )

            status = "✅" if atingiu_meta else "❌"

            embed.add_field(
                name=f"{usuario} ({status})",
                value=f"nitrox: {farm_nitrox}, chavinha: {farm_chavinha}, disco: {farm_disco}, suspensão: {farm_suspensao}",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def comissao(self, ctx):
        embed = discord.Embed(title="💰 Comissão dos Membros", color=discord.Color.gold())
        for uid, user_data in Farms.items():
            usuario = user_data.get("usuario", "Desconhecido")
            total_vendas = sum(user_data.get("vendas", []))
            pagamento = round(total_vendas * 0.30, 2)
            embed.add_field(name=usuario, value=f"Valor a receber: R${pagamento}", inline=False)
        await ctx.send(embed=embed)


class FarmModal(discord.ui.Modal, title="Registro de Farm"):
    tipo = discord.ui.TextInput(label="Tipo", placeholder="nitrox, chavinha, disco, suspensao")
    quantidade = discord.ui.TextInput(label="Quantidade", placeholder="Ex: 10")

    def __init__(self, user_id, user_name):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name

    async def on_submit(self, interaction: discord.Interaction):
        tipo = self.tipo.value.strip().lower()
        try:
            qtd = int(self.quantidade.value)
            if qtd <= 0 or tipo not in {"nitrox", "chavinha", "disco", "suspensao"}:
                raise ValueError
        except ValueError:
            return await interaction.response.send_message("❌ Dados inválidos.", ephemeral=True)

        uid = str(self.user_id)
        Farms.setdefault(uid, {
            "usuario": self.user_name,
            "farm": [],
            "vendas": [],
            "sujo": []
        })
        for campo in ["nitrox", "chavinha", "disco", "suspensao"]:
            Farms[uid].setdefault(campo, 0)

        Farms[uid][tipo] += qtd
        Farms[uid]["farm"].append({"item": tipo, "quantidade": qtd})
        salva(FARMS_FILE, Farms)

        await interaction.response.send_message(f"✅ Farm registrado: {tipo} x{qtd}", ephemeral=True)


class VendaModal(discord.ui.Modal, title="Registro de Venda"):
    valor = discord.ui.TextInput(label="Valor", placeholder="Ex: 100.50")

    def __init__(self, user_id, user_name):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name

    async def on_submit(self, interaction: discord.Interaction):
        try:
            v = float(self.valor.value)
            if v <= 0:
                raise ValueError
        except ValueError:
            return await interaction.response.send_message("❌ Valor inválido.", ephemeral=True)

        uid = str(self.user_id)
        Farms.setdefault(uid, {"usuario": self.user_name, "farm": [], "vendas": [], "sujo": []})
        Farms[uid]["vendas"].append(v)

        Financeiro["entradas"].append(v)
        pay = round(v * 0.30, 2)
        Financeiro["saidas"].append(pay)

        salva(FARMS_FILE, Farms)
        salva(FINANCE_FILE, Financeiro)

        await interaction.response.send_message(f"✅ Venda de R${v} registrada. Comissão: R${pay}.", ephemeral=True)


class SujoModal(discord.ui.Modal, title="Dinheiro Sujo"):
    valor = discord.ui.TextInput(label="Valor", placeholder="Ex: 50.00")

    def __init__(self, user_id, user_name):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name

    async def on_submit(self, interaction: discord.Interaction):
        try:
            v = float(self.valor.value)
            if v <= 0:
                raise ValueError
        except ValueError:
            return await interaction.response.send_message("❌ Valor inválido.", ephemeral=True)

        uid = str(self.user_id)
        Farms.setdefault(uid, {"usuario": self.user_name, "farm": [], "vendas": [], "sujo": []})
        Farms[uid]["sujo"].append(v)
        salva(FARMS_FILE, Farms)

        await interaction.response.send_message(f"✅ Dinheiro sujo R${v} registrado.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Farm(bot))
