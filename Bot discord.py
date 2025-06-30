# bot.py
import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user} (ID: {bot.user.id})")

async def load_extensions():
    # Usa caminho absoluto baseado no local deste arquivo
    cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')

    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start("insira seu token")

if __name__ == "__main__":
    asyncio.run(main())