import discord
from discord.ext import commands
import platform # Biblioteca para saber onde o bot está a rodar

# Configura as permissões obrigatórias
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot ligado com sucesso como: {bot.user}')

# Comando !botinfo
@bot.command()
async def botinfo(ctx):
    # Procura as informações da aplicação para descobrir o dono dinamicamente
    app_info = await bot.application_info()
    dono = app_info.owner
    
    # Deteta o sistema operativo de forma amigável
    sistema_operativo = platform.system()
    if sistema_operativo == "Linux" and "android" in platform.release().lower():
        onde_roda = "📱 Telemóvel (Termux / Android)"
    elif sistema_operativo == "Linux":
        onde_roda = "🐧 Servidor Linux / VPS"
    elif sistema_operativo == "Windows":
        onde_roda = "💻 Computador (Windows)"
    else:
        onde_roda = f"⚙️ {sistema_operativo}"

    # Criar uma mensagem bonita (Embed)
    embed = discord.Embed(
        title="ℹ️ Informações do Bot", 
        color=discord.Color.blue()
    )
    embed.add_field(name="👑 Dono do Bot", value=f"{dono.name} ({dono.mention})", inline=False)
    embed.add_field(name="📍 Onde está a rodar?", value=onde_roda, inline=False)
    embed.add_field(name="🐍 Versão do Python", value=platform.python_version(), inline=True)
    embed.add_field(name="📚 Biblioteca", value=f"discord.py v{discord.__version__}", inline=True)
    
    # Envia a resposta para o canal
    await ctx.send(embed=embed)

# Coloca aqui o teu Token secreto do Discord Developer Portal
bot.run('')
