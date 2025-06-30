import discord
from discord.ext import commands
from utils import carrega, enviar_log

REGISTROS_MEMBROS = "hierarquia4m.json"
CANAL_LOGS_ID = 1382393091545366598

Lista_membros = carrega(REGISTROS_MEMBROS, [])


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx):
        usuario = next((r for r in Lista_membros if r['discord_id'] == ctx.author.id), None)
        if usuario is None:
            return await ctx.send("❌ Você precisa se registrar primeiro com `!registro`.")

        view = discord.ui.View()

        async def criar_ticket(interaction: discord.Interaction):
            categoria_nome = usuario['nome']
            if discord.utils.get(ctx.guild.categories, name=categoria_nome):
                return await interaction.response.send_message("🎫 Ticket já existe.", ephemeral=True)

            cat = await ctx.guild.create_category(categoria_nome)
            chat = await ctx.guild.create_text_channel("⚫￤chat", category=cat)
            provas = await ctx.guild.create_text_channel("🔴￤farm", category=cat)

            await cat.set_permissions(ctx.guild.default_role, view_channel=False)
            await chat.set_permissions(ctx.author, view_channel=True)
            await provas.set_permissions(ctx.author, view_channel=True)

            await interaction.response.send_message(f"🎫 Ticket criado em `{categoria_nome}`!", ephemeral=True)
            await enviar_log(ctx.guild, f"🎫 Ticket criado para {ctx.author.mention}.", canal_id=CANAL_LOGS_ID)

        botao = discord.ui.Button(label="Crie seu chat", style=discord.ButtonStyle.green)
        botao.callback = criar_ticket
        view.add_item(botao)

        await ctx.send("Clique para criar seu ticket:", view=view)


async def setup(bot):
    await bot.add_cog(Ticket(bot))
