import os
import platform
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Carrega as variáveis de ambiente a partir do ficheiro .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Configura as permissões obrigatórias
intents = discord.Intents.default()
intents.message_content = True

class MeuBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Carrega automaticamente todos os ficheiros .py dentro da pasta 'cogs' ao iniciar
        if os.path.exists("./cogs"):
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    cog_name = f"cogs.{filename[:-3]}"
                    await self.load_extension(cog_name)
                    print(f"📦 Módulo carregado: {filename}")
        else:
            print("⚠️ A pasta 'cogs' não foi encontrada!")

    async def on_ready(self):
        print(f"✅ Bot ligado com sucesso como: {self.user}")

bot = MeuBot()

# --- COMANDOS DE GESTÃO DE COGS ---

@bot.command(name="load")
@commands.is_owner() # Podes remover se quiseres que qualquer pessoa use (não recomendado)
async def load_cog(ctx, extension: str):
    """Carrega um módulo que esteja desativado."""
    try:
        await bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"✅ Módulo `cogs.{extension}` carregado com sucesso!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao carregar: `{e}`")

@bot.command(name="unload")
@commands.is_owner()
async def unload_cog(ctx, extension: str):
    """Desativa um módulo temporariamente."""
    try:
        await bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"⚠️ Módulo `cogs.{extension}` desativado com sucesso!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao desativar: `{e}`")

@bot.command(name="reload")
async def reload_cog(ctx, extension: str):
    """Recarrega um módulo após alterares o código no GitHub e fazeres git pull."""
    try:
        await bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"🔄 Módulo `cogs.{extension}` recarregado com sucesso! As alterações já estão ativas.")
    except Exception as e:
        await ctx.send(f"❌ Erro ao recarregar: `{e}`")

# Inicia o bot com o token seguro carregado do ambiente
bot.run(TOKEN)
