import os
import platform
import random
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


# --- COMANDOS DE UTILIDADE E GESTÃO DO SERVIDOR ---

@bot.command(name="ping", help="Mostra a latência atual do bot.")
async def ping(ctx):
    latencia = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! A latência é de **{latencia}ms**.")

@bot.command(name="sync", help="Sincroniza os slash commands globalmente ou por guild.")
@commands.is_owner()
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
    
    apagadas = await ctx.channel.purge(limit=quantidade + 1)
    msg = await ctx.send(f"🧹 Foram apagadas **{len(apagadas) - 1}** mensagens.")
    await msg.delete(delay=4)

@bot.command(name="desligar", aliases=["shutdown"], help="Desliga o bot com segurança.")
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("🔌 A desligar o bot... Até breve!")
    await bot.close()


# --- NOVOS COMANDOS DE DIVERSÃO E UTILIDADE ---

@bot.command(name="avatar", help="Mostra o avatar de um utilizador.")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    
    embed = discord.Embed(
        title=f"Avatar de {member.name}",
        color=discord.Color.blue()
    )
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="dado", aliases=["roll"], help="Rola um dado (ex: !dado 6 para um dado de 6 faces).")
async def rolar_dado(ctx, lados: int = 6):
    if lados < 2:
        await ctx.send("⚠️ O dado precisa de ter pelo menos 2 lados!")
        return
    resultado = random.randint(1, lados)
    await ctx.send(f"🎲 {ctx.author.mention}, o resultado do dado (1-{lados}) foi: **{resultado}**")

@bot.command(name="say", help="Faz o bot repetir uma mensagem e apaga a original.")
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, mensagem: str):
    await ctx.message.delete()
    await ctx.send(mensagem)

@bot.command(name="userinfo", aliases=["perfil"], help="Mostra informações sobre um utilizador.")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    
    criacao = member.created_at.strftime("%d/%m/%Y às %H:%M")
    entrada = member.joined_at.strftime("%d/%m/%Y às %H:%M") if member.joined_at else "Desconhecido"
    
    embed = discord.Embed(title=f"Informações de {member.name}", color=member.color)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Conta Criada a", value=criacao, inline=False)
    embed.add_field(name="Entrou no Servidor a", value=entrada, inline=False)
    
    await ctx.send(embed=embed)


# --- TRATAMENTO DE ERROS ---

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
