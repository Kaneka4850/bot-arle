# Parcerias
import discord
from discord.ext import commands
from utils import carrega, salva

PARCEIROS_FILE = "parceriasda4m.json"

Parceiros = carrega(PARCEIROS_FILE, {
    "arma": [], "munição": [], "lavagem": [],
    "drogas": [], "desmanche": [], "legal": []
})


class ParceirosCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addparceiro(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("❌ Apenas admins podem cadastrar parceiros.")

        class TipoSelect(discord.ui.Select):
            def __init__(self):
                options = [
                    discord.SelectOption(label="Arma", value="arma"),
                    discord.SelectOption(label="Munição", value="munição"),
                    discord.SelectOption(label="Lavagem", value="lavagem"),
                    discord.SelectOption(label="Drogas", value="drogas"),
                    discord.SelectOption(label="Desmanche", value="desmanche"),
                    discord.SelectOption(label="Legal", value="legal"),
                ]
                super().__init__(placeholder="Selecione o setor", options=options)

            async def callback(self, interaction: discord.Interaction):
                tipo = self.values[0]
                await interaction.response.send_modal(AddParceiroModal(tipo))

        class TipoView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)
                self.add_item(TipoSelect())

        await ctx.send("Selecione o setor para cadastrar parceiro:", view=TipoView())

    @commands.command()
    async def parcerias(self, ctx):
        class Menu(discord.ui.Select):
            def __init__(self):
                options = [
                    discord.SelectOption(label="Arma", value="arma", emoji="🔫"),
                    discord.SelectOption(label="Munição", value="munição", emoji="💥"),
                    discord.SelectOption(label="Lavagem", value="lavagem", emoji="🧼"),
                    discord.SelectOption(label="Drogas", value="drogas", emoji="💊"),
                    discord.SelectOption(label="Desmanche", value="desmanche", emoji="🧰"),
                    discord.SelectOption(label="Legal", value="legal", emoji="🏥"),
                ]
                super().__init__(placeholder="Selecione uma parceria...", options=options)

            async def callback(self, interaction: discord.Interaction):
                tipo = self.values[0]
                dados = Parceiros.get(tipo, [])
                if not dados:
                    await interaction.response.send_message(f"📭 Nenhum parceiro em **{tipo}**.", ephemeral=True)
                    return

                resposta = f"📋 **Parceiros de {tipo.capitalize()}**:\n\n"
                for p in dados:
                    resposta += (
                        f"👤 **{p['nome']}**\n"
                        f"📱 Telefone: {p['telefone']}\n"
                        f"🔖 Produto: {p['produto']}\n"
                        f"🏷️ Fac: {p['fac']}\n"
                        f"📍 Bairro: {p['bairro']}\n\n"
                    )
                await interaction.response.send_message(resposta, ephemeral=True)

        class View(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                self.add_item(Menu())

        embed = discord.Embed(
            title="🤝 Parcerias",
            description="Selecione o setor para ver os parceiros.",
            color=discord.Color.blurple()
        )
        await ctx.send(embed=embed, view=View())


class AddParceiroModal(discord.ui.Modal):
    def __init__(self, tipo):
        super().__init__(title=f"Adicionar Parceiro - {tipo.capitalize()}")
        self.tipo = tipo

        self.nome = discord.ui.TextInput(label="Nome", max_length=100)
        self.telefone = discord.ui.TextInput(label="Telefone", max_length=30)
        self.produto = discord.ui.TextInput(label="Produto", max_length=100)
        self.fac = discord.ui.TextInput(label="Facção/Parceiro", max_length=100)
        self.bairro = discord.ui.TextInput(label="Bairro", max_length=100)

        self.add_item(self.nome)
        self.add_item(self.telefone)
        self.add_item(self.produto)
        self.add_item(self.fac)
        self.add_item(self.bairro)

    async def on_submit(self, interaction: discord.Interaction):
        Parceiros[self.tipo].append({
            "nome": self.nome.value,
            "telefone": self.telefone.value,
            "produto": self.produto.value,
            "fac": self.fac.value,
            "bairro": self.bairro.value
        })
        salva(PARCEIROS_FILE, Parceiros)
        await interaction.response.send_message("✅ Parceiro cadastrado.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(ParceirosCog(bot))
