#base de dados
from dotenv import load_dotenv
import os
#bot
import logging
import discord
from discord.ext import commands

#secrets
load_dotenv()
token =os.getenv('DISCORD_BOT_TOKEN')


#intents(todas as permissoes via intents, temos que habilitar manualmente)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

#cargos(para realizar algo especifico)
player = "Player"
GM = "GM"

#region configurando_bot
bot = commands.Bot(command_prefix='!',intents=intents,case_insensitive=True)#!comando -> intent
@bot.event
#sempre que for on_ready é quando ele iniciar
async def on_ready():
    for guild in bot.guilds:  # percorre todos os servidores
        canal = discord.utils.get(guild.text_channels, name="geral")
        if canal:
            await canal.send("Bot esta online e foi atualizado!")

@bot.event
async def on_member_join(member):
    #manda no pv deste jeito member.send()
    canal_geral = discord.utils.get(member.guild.text_channels, name="geral")
    cargo_player = discord.utils.get(member.guild.roles, name="Player")
    
    if cargo_player:
        await member.add_roles(cargo_player)
    await canal_geral.send(f"""
                           Bem vindo {member.name} ao servidor do rpg!
                           qualquer dúvida digite !comandos para a lista de comandos
                           {member.name} foi promovida para Player
    """)

@bot.event
#moderar mensagens(algumas como meme outras não)
async def on_message(msg):#somente 1 parametro senão nn funciona
    member = msg.author#tem que definir manualmente
    #evitar auto reply
    if msg.author == bot.user:
        return
    #piada
    if "não vou participar da sessão" in msg.content.lower():
        try:
            await member.send("vai sim")
            await msg.delete()
            await msg.channel.send(f"{member.mention} confirmou que vai participar da sessão")
        except:
            print("algum erro")
    await bot.process_commands(msg)#lidar com todas as outras mensagens

#endregion configurando_bot
#comando(ctx) ctx=contexto -> !comando

#region Gm
#comandos GM
@bot.command()
@commands.has_role(GM)
async def dia(ctx,*,pergunta=None):#ja vai fazer a pegunta
    embed = discord.Embed(title="Dia da sessão",description=f"Qual dia será a sessão\n\n Sábado\n Domingo\n Não posso esse fim de semana\n feriado(se tiver)")
    votacao = await ctx.send(embed=embed)
    await votacao.add_reaction("🔥")
    await votacao.add_reaction("1️⃣")
    await votacao.add_reaction("2️⃣")
    await votacao.add_reaction("3️⃣")
    await votacao.add_reaction("4️⃣")
@dia.error
async def dia_erro(ctx,error):
    member = ctx.author
    #se nn tiver o cargo
    if isinstance(error,commands.MissingRole):
        await ctx.send(f"{member.mention} não é um GM comando exclusivo para GM")
        await ctx.add_reaction("✅")
        await ctx.add_reaction("❌")
#endregion Gm

#region comandos_gerais
#comandos gerais
@bot.command()
async def comandos(ctx):
    member = ctx.author
    await ctx.send(f"""{member.mention} a lista de comandos do bot é:
                   - comandos globais: 
                   !comandos mostra a lista de comandos
                   !virar_player (mais para quem ja estava no server antes do bot) adicionar este cargo na tua conta
                   !virar_mestre (mais para quem ja estava no server antes do bot) adicionar este cargo na tua conta
                   - comandos player:
                   !sair remove cargo de player(vc ainda pode participar no chat)
                   - comandos GM:        
                   !dia bot gera poll para o dia da sessão
                           """)
@bot.command()
async def poll(ctx,*,pergunta):
    embed = discord.Embed(title="Dia da sessão",description=pergunta)
    votacao = await ctx.send(embed=embed)
    await ctx.add_reaction("✅")
    await ctx.add_reaction("❌")

#para usuarios antigos do server se tornarem players/mestres
@bot.command()
async def virar_player(ctx):
    member = ctx.author
    cargo_player = discord.utils.get(ctx.guild.roles, name=player)

    if not cargo_player:
        await ctx.send("Cargo Player não encontrado.")
        return

    if cargo_player in member.roles:
        await ctx.send(f"{member.mention} você já é Player.")
        return

    try:
        await member.add_roles(cargo_player)
        await ctx.send(f"{member.mention} agora é Player!")
    except discord.Forbidden:
        await ctx.send("Não tenho permissão para adicionar cargos.")

@bot.command()
async def virar_mestre(ctx):
    member = ctx.author
    cargo_mestre = discord.utils.get(ctx.guild.roles, name=GM)

    if not cargo_mestre:
        await ctx.send("Cargo MESTRE não encontrado.")
        return

    if cargo_mestre in member.roles:
        await ctx.send(f"{member.mention} você já é MESTRE.")
        return

    try:
        await member.add_roles(cargo_mestre)
        await ctx.send(f"{member.mention} agora é MESTRE!")
    except discord.Forbidden:
        await ctx.send("Não tenho permissão para adicionar cargos.")
#endregion comandos_gerais

#region player
#comandos player
@bot.command()
@commands.has_role(player)
async def sair(ctx):
    member = ctx.author
    cargo= discord.utils.get(ctx.guild.roles, name=player)
    #remover cargo
    if cargo:
        await member.remove_roles(cargo)
    await ctx.send(f"{member.mention} saindo da campanha seu cargo não é mais {player}")
@sair.error
async def sair_erro(ctx,error):
    member = ctx.author
    #se nn tiver o cargo
    if isinstance(error,commands.MissingRole):
        await ctx.send(f"{member.mention} não é {player} então não pode sair da campanha")
#endregion player

bot.run(token)