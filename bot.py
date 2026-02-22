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

#configurando bot
log = logging.FileHandler(filename='bot.log',encoding='utf-8',mode='w')
#intents(todas as permissoes via intents, temos que habilitar manualmente)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

#cargos
player = "Player"
GM = "GM"
#bot
bot = commands.Bot(command_prefix='!',intents=intents,case_insensitive=True)#!comando -> intent
@bot.event
#sempre que for on_ready é quando esta online
async def on_ready():
    print(f"bot {bot.user.name} esta online")

@bot.event
async def on_member_join(member):
    #manda no pv deste jeito member.send()
    canal_geral = discord.utils.get(member.guild.text_channels, name="geral")
    await canal_geral.send(f"""Bem vindo {member.name} ao servidor do rpg!
                           qualquer dúvida digite !comandos para a lista de comandos
                           vamos criar sua ficha digite !ficha para começar""")

@bot.event
#moderar mensagens
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
        
#comando(ctx) ctx=contexto -> !comando

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


async def aviso(guild,tipo):
    #manda no pv deste jeito member.send()
    canal_geral = discord.utils.get(guild.text_channels, name="geral")
    if tipo == "inicio":
        await canal_geral.send(f"""Sessão prestes a iniciar""")
    elif tipo == "fim":
        await canal_geral.send(f"""Sessão finalizada""")
    else:
        await canal_geral.send(f"""aaaaa""")


#comandos gerais
@bot.command()
async def comandos(ctx):
    member = ctx.author
    await ctx.send(f"""{member.mention} a lista de comandos do bot é:
                   - comandos globais: 
                   !comandos esta mensagem
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

#rodar bot

bot.run(token)

