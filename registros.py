import discord
from discord.ext import commands
from discord import ui, Interaction
from utils import carrega, salva, enviar_log

import re

CANAL_LOGS_ID = 1382393091545366598
CARGO_APROVADOR_ID = 1382398046087680080
REGISTROS_MEMBROS = "hierarquia4m.json"

Lista_membros = carrega(REGISTROS_MEMBROS, [])


class Registro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="listarcomandos2")
    async def listar_comandos2(self, ctx):
        descricoes = {
            "registro": "Registre-se na fac.",
            "listar_registros": "Veja a lista de registros aprovados (apenas admins).",
            "demitir": "Demitir um membro (apenas admins)."
        }
        mensagem = "**Comandos disponíveis:**\n\n"
        for cmd, desc in descricoes.items():
            mensagem += f"!{cmd} - {desc}\n"
        await ctx.send(mensagem)

    @commands.command()
    async def registro(self, ctx):
        view = discord.ui.View()

        async def abrir_modal(interaction: discord.Interaction):
            await interaction.response.send_modal(RegistroModal())

        botao = discord.ui.Button(label="Registrar", style=discord.ButtonStyle.green)
        botao.callback = abrir_modal
        view.add_item(botao)

        await ctx.send("Clique para se registrar:", view=view)

    @commands.command(name="listar_registros")
    async def listar_registros(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("❌ Sem permissão.")
            return

        registros_aprovados = [r for r in Lista_membros if r.get("aprovado")]

        if not registros_aprovados:
            await ctx.send("Nenhum registro aprovado.")
            return

        for i in range(0, len(registros_aprovados), 5):
            bloco = registros_aprovados[i:i+5]
            embed = discord.Embed(title="Registros aprovados", color=discord.Color.green())
            for idx, registro in enumerate(bloco, start=i+1):
                embed.add_field(
                    name=f"{idx}. {registro['usuario']}",
                    value=f"Nome: {registro['nome']}\nID: {registro['id']}\nTelefone: {registro['telefone']}",
                    inline=False
                )
            await ctx.send(embed=embed)

    @commands.command()
    async def demitir(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("❌ Apenas admins.")
            return

        view = discord.ui.View()

        async def abrir_modal(interaction: discord.Interaction):
            await interaction.response.send_modal(DemitirModal())

        botao = discord.ui.Button(label="Confirmar demissão", style=discord.ButtonStyle.danger)
        botao.callback = abrir_modal
        view.add_item(botao)

        await ctx.send("Clique para demitir um membro:", view=view)


class RegistroModal(discord.ui.Modal, title="Registro"):
    nome = discord.ui.TextInput(label="Nome", max_length=32)
    user_id = discord.ui.TextInput(label="ID", max_length=32)
    telefone = discord.ui.TextInput(label="Telefone (000-000)", max_length=10)

    async def on_submit(self, interaction: discord.Interaction):
        telefone_fmt = self.telefone.value
        if not re.fullmatch(r"\d{3}-\d{3}", telefone_fmt):
            return await interaction.response.send_message("Formato inválido.", ephemeral=True)

        registro = {
            "nome": self.nome.value,
            "id": self.user_id.value,
            "telefone": telefone_fmt,
            "usuario": interaction.user.name,
            "discord_id": interaction.user.id,
            "aprovado": False
        }
        Lista_membros.append(registro)
        salva(REGISTROS_MEMBROS, Lista_membros)

        await interaction.response.send_message("Registro enviado para aprovação.", ephemeral=True)

        view = discord.ui.View()

        async def aprovar(inter_: discord.Interaction):
            membro = inter_.user
            if not membro.guild_permissions.administrator and CARGO_APROVADOR_ID not in [r.id for r in membro.roles]:
                return await inter_.response.send_message("Sem permissão.", ephemeral=True)

            for r in Lista_membros:
                if r["discord_id"] == registro["discord_id"]:
                    r["aprovado"] = True
                    break
            salva(REGISTROS_MEMBROS, Lista_membros)
            await inter_.response.edit_message(content="Registro aprovado!", view=None)
            await enviar_log(inter_.guild, f"{registro['usuario']} aprovado.", canal_id=CANAL_LOGS_ID)

        botao = discord.ui.Button(label="Aprovar", style=discord.ButtonStyle.green)
        botao.callback = aprovar
        view.add_item(botao)

        await enviar_log(interaction.guild, f"Novo registro pendente de aprovação.", view=view, canal_id=CANAL_LOGS_ID)


class DemitirModal(discord.ui.Modal, title="Demitir Membro"):
    discord_id = discord.ui.TextInput(label="ID Discord", max_length=18)

    async def on_submit(self, interaction: discord.Interaction):
        did = int(self.discord_id.value)
        usr = next((r for r in Lista_membros if r['discord_id'] == did), None)
        if not usr:
            return await interaction.response.send_message("Usuário não encontrado.", ephemeral=True)

        Lista_membros.remove(usr)
        salva(REGISTROS_MEMBROS, Lista_membros)
        await interaction.response.send_message(f"{usr['usuario']} demitido.", ephemeral=True)
        await enviar_log(interaction.guild, f"{usr['usuario']} demitido.", canal_id=CANAL_LOGS_ID)


async def setup(bot):
    await bot.add_cog(Registro(bot))
