import os
import platform
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

class MeuBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Procura na pasta atual (raiz) por ficheiros que comecem com "cog_"
        for filename in os.listdir("./"):
            if filename.startswith("cog_") and filename.endswith(".py"):
                cog_name = filename[:-3] # Remove o .py
                await self.load_extension(cog_name)
                print(f"📦 Módulo carregado: {filename}")

    async def on_ready(self):
        print(f"✅ Bot ligado com sucesso como: {self.user}")

bot = MeuBot()

# --- COMANDOS DE GESTÃO ---

@bot.command(name="load")
async def load_cog(ctx, extension: str):
    try:
        await bot.load_extension(extension)
        await ctx.send(f"✅ Módulo `{extension}` carregado com sucesso!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao carregar: `{e}`")

@bot.command(name="unload")
async def unload_cog(ctx, extension: str):
    try:
        await bot.unload_extension(extension)
        await ctx.send(f"⚠️ Módulo `{extension}` desativado com sucesso!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao desativar: `{e}`")

@bot.command(name="reload")
async def reload_cog(ctx, extension: str):
    try:
        await bot.reload_extension(extension)
        await ctx.send(f"🔄 Módulo `{extension}` recarregado com sucesso!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao recarregar: `{e}`")

bot.run(TOKEN)
