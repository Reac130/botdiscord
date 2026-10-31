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

# --- COMANDOS DE GESTÃO DE COGS ---

@bot.command(name="load", help="Carrega um módulo (cog) existente.")
async def load_cog(ctx, extension: str):
    try:
        await bot.load_extension(extension)
        await ctx.send(f"✅ Módulo `{extension}` carregado com sucesso!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao carregar: `{e}`")

@bot.command(name="unload", help="Desativa um módulo (cog).")
async def unload_cog(ctx, extension: str):
    try:
        await bot.unload_extension(extension)
        await ctx.send(f"⚠️ Módulo `{extension}` desativado com sucesso!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao desativar: `{e}`")

@bot.command(name="reload", help="Recarrega um módulo (cog) para aplicar alterações.")
async def reload_cog(ctx, extension: str):
    try:
        await bot.reload_extension(extension)
        await ctx.send(f"🔄 Módulo `{extension}` recarregado com sucesso!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao recarregar: `{e}`")


# --- NOVOS COMANDOS ADICIONADOS ---

@bot.command(name="ping", help="Mostra a latência atual do bot.")
async def ping(ctx):
    latencia = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! A latência é de **{latencia}ms**.")

@bot.command(name="sync", help="Sincroniza os slash commands globalmente ou por guild.")
@commands.is_owner() # Opcional: Garante que apenas o dono do bot pode usar
async def sync_commands(ctx):
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"🔄 Sincronizados **{len(synced)}** comandos slash com sucesso!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao sincronizar comandos: `{e}`")

@bot.command(name="limpar", aliases=["clear"], help="Apaga um número específico de mensagens.")
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, quantidade: int = 5):
    if quantidade <= 0:
        await ctx.send("⚠️ Por favor, indica um número maior que 0.")
        return
    
    # Apaga as mensagens (+1 para incluir a mensagem do próprio comando)
    apagadas = await ctx.channel.purge(limit=quantidade + 1)
    
    msg = await ctx.send(f"🧹 Foram apagadas **{len(apagadas) - 1}** mensagens.")
    await msg.delete(delay=4) # Apaga o aviso passado 4 segundos

@bot.command(name="desligar", aliases=["shutdown"], help="Desliga o bot com segurança.")
@commands.is_owner() # Apenas o dono do bot configurado no Developer Portal pode usar
async def shutdown(ctx):
    await ctx.send("🔌 A desligar o bot... Até breve!")
    await bot.close()

# Tratamento de erros para comandos restritos ao dono ou com permissões
@limpar.error
async def limpar_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Não tens permissão para gerir mensagens (`Gerir Mensagens`).")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Por favor, introduz um número válido.")

@shutdown.error
@sync_commands.error
async def owner_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("❌ Apenas o dono do bot pode executar este comando.")

bot.run(TOKEN)
