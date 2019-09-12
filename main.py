import discord
from discord.ext        import commands
from rcon               import insert_data
from rcon               import select_data
from rcon               import rcon_console
from datetime           import datetime
from _utils             import tools
import os
import keep_alive

# LINK DE CONVITE
#https://discordapp.com/oauth2/authorize?&client_id=609902143222054955&scope=bot&permissions=0
bot = commands.Bot(command_prefix='!', description='Um bot de gestão/integração para servidores Ark')
client = discord.Client()


@bot.event
async def on_ready():
    print('Bot em operação, aguardando comandos  -  ' + str(datetime.now()))

# REGISTRA NO CANAL DE TEXTO 'PORTA-DOS-FUNDOS' A SAIDA DO USUÁRIO
@bot.event
async def on_member_remove(member):
    nome_canal = 'porta-dos-fundos'
    servidor = member.guild
    id_canal = discord.utils.get(bot.get_all_channels(), guild__name=servidor.name, name=nome_canal)
    channel = bot.get_channel(id_canal.id)
    report = '## Dados do usuário:  ' + f'{member}' + '\n## Nick Server:  ' + str(member.nick) + '\n## Entrou no servidor em:  ' + str(member.joined_at) + '\n## Saiu do servidor em:  ' + str(datetime.now())
    await channel.send(report)

#@bot.event
#async def on_message(message):
#    #IGNORA SE AUTOR DA MENSAGEM FOR O BOT
#    if message.author == bot.user:
#        pass

@bot.command()
async def version(ctx):
    await ctx.send("Bot Version 1.0 \nAuthor: Selmo Rodrigues \nDate release: 2019/08/31 \n e-mail contact: selmobe.rodrigues@outlook.com.br")

@bot.command()
async def broadcast_allservers(ctx, *, string_message):
    id_guild = '517617870612725763'
    if string_message != None:
        if ctx.author.nick == None:
            author_message = ctx.author.name
        else:
            author_message = ctx.author.nick
        
        _message =  string_message + ' | ' + author_message
        rcon_console.broadcast_all_servers(id_guild, _message)
      
@bot.command(name='register_server_ark')
async def admin_register_ark_server(ctx, ip_server, rcon_port, rcon_password, mode_server, map_name, map_patreon, description):
    msg = insert_data.set_register_server_ark(ctx.guild.id, ip_server, rcon_port, rcon_password, mode_server, map_name, map_patreon, description)
    await ctx.send('Resource still under development, being released for use in the near future')
    return
    await ctx.message.delete()
    if msg == 'successfully':
        msg = 'Server successfully registered: IP Server: ' + ip_server + ':' + str(rcon_port) + ' | Map: ' + map_name + ' | Patreon Only: ' + map_patreon
    else:
        msg = 'Error registering server, please contact support'
    await ctx.send(msg)

@bot.command(description="Comando utilizado para registrar o id64 por outro usuário")
async def admin_register_id64(ctx,  member:discord.Member, id64_steam):
    print(">> Comando para registro de id64 Steam utilizado por terceiros _admin_register_id64_ param: " + str(id64_steam) + ' ' + member.name)
    if member.nick != None:
        register_member = member.nick
    else:
        register_member = member.name + '#' + member.discriminator
    
    msg = rcon_console.register_idsteam(register_member, id64_steam, member.id)
    if msg == 'successfully':
        msg = 'User ' + register_member + ' successfully registered!'
    else:
        msg = rcon_console.get_id64_steam(member.id)
        if len(msg) > 0:
            msg = 'User already has registration in the system, no new registration required'
        else:
            msg = 'Failed to register user, please contact support!'
    await ctx.send(msg)

@bot.command(description="Imprime em tela as regras associadas ao usuário que executou o comando")
async def print_roles(ctx):
    """ Imprimir no chat as regras atribuidas ao usuário """
    await ctx.send('Resource still under development, being released for use in the near future')
    return
    print(">> Comando de listagem de regras executado _print_roles_")
    if ctx.author.nick == None:
        await ctx.send(ctx.author.name)
    else:
        await ctx.send(ctx.author.nick)
    
    for x in ctx.author.roles:
        if str(x.name) != "@everyone":
            await ctx.send(x)

@bot.command(description='Registra o server no banco de dados')
async def register_server(ctx):
    """Executa o registro do servidor Discord no banco de dados"""
    print('>> Comando de registro de servidor executado _register_server_')
    msg = insert_data.set_register_guild(ctx.guild.id, ctx.guild.name)
    if str(msg) == 'successfully':
        msg = 'Success registering ID Server: ' + str(ctx.guild.id) + ' | Name server: ' + ctx.guild.name
    else:
        msg = 'Error registering server, please contact support for more information.'
    await ctx.send(msg)

@bot.command(description=' Remove do banco de dados o servidor no qual o comando for utilizado')
async def remove_register_server(ctx):
    print(">> Comando de remoção de registro de Servidor Discord executado _unregister_server_")
    x = insert_data.set_unregister_guild(ctx.guild.id)
    if str(x) == 'successfully':
        await ctx.send('Success unregistering ID Server: ' + str(ctx.guild.id) + ' | Name server: ' + ctx.guild.name)
    else:
        await ctx.send('Error unregistering server, please contact support for more information.')

@bot.command(description=' Registra o ID64 Steam do usuário no banco de dados para facilitar a desova de dinos ')
async def register_id64(ctx, id64_steam):
    print(">> Comando para registrar id64 Steam executado _register_id64_ param: " + str(id64_steam))
    if ctx.author.nick != None:
        register_member = ctx.author.nick
    else:
        register_member = ctx.author.name + '#' + ctx.author.discriminator
    msg = rcon_console.register_idsteam(register_member, id64_steam, str(ctx.author.id))
    if msg == 'successfully':
        msg = 'User ' + register_member + ' successfully registered'
    else:
        msg = rcon_console.get_id64_steam(ctx.author.id)
        if len(msg) > 0:
            msg = 'User already has registration in the system, no new registration required'
        else:
            msg = 'Failed to register user, please contact support!'
    await ctx.message.delete()
    await ctx.send(msg)

# Remover futuramente, comando considerado inutil
@bot.command(description='A partir do id64 do usuário e id do servidor, retorna a atual posição gps do usuário(param: id64_user - id_mapa_server (para localizar o id_mapa_server utiize o comando LISTA_SERVIDORES))')
async def get_user_pos(ctx, id64_user, id_mapa_server):
    """Consulta posição atual do jogador"""
    await ctx.send('Resource still under development, being released for use in the near future')
    return
    print(">> Comando de localizar jogador executado _get_user_pos_")
    if id64_user != '' and id_mapa_server != '':
        await ctx.send('Consultando dados, por favor aguarde...')
        saida = rcon_console.get_player_pos_gps(ctx.guild.id,id64_user, int(id_mapa_server))
        await ctx.send(saida)
        print('erro:' + saida)
    else:
        await ctx.send('Para esta consulta é necessário informar o Id64 e o servidor/mapa a ser consultado!!')

@bot.command(description='Recupera a lista com todos os jogadores ativos no servidor(Não necessita de parâmetros)')
async def players_online(ctx):
    """Lista jogadores ativos nos servidores"""
    print(">> Comando de listagem de jogadores executado _players_online_")
    id_guild = '517617870612725763'
    #id_guild = str(ctx.guild.id)
    list_servers = rcon_console.get_players_online(id_guild)

    for server in list_servers:
        name_server = server[0]
        player = server[1]
        msg = '```' + 'Map: ' + name_server + player[0] + '```'
        await ctx.send(msg)

@bot.command(name='get_server_list', description='Lista todos os servidores ARk atribuidos a guilda atual')
async def _server_list(ctx):
    """Lista todos os servidores Mapas Ark cadastrados"""
    print(">> Comando de listagem de servidores executada _server_list_")
    id_guild = '517617870612725763'#str(ctx.guild.id)
    list_servers = rcon_console.get_list_servers(id_guild)

    if len(list_servers) > 0:
        for server in list_servers:
            await ctx.send('```css' + server + '\n```')
    else:
        await ctx.send("Not found servers")

@bot.command(name='get_server_status', description='Recupera os status de todos os servidores da guilda atual (velocidade de retorna dependente do servidor')
async def _servers_status(ctx):
    """Recupera os status de todos os servidores"""
    print(">> Comando de verificação de estatus executado _get_servers_status_")
    id_guild = '517617870612725763'#str(ctx.guild.id)
    guild_list_server = select_data.get_guild_servers(id_guild)
    
    for id_server in guild_list_server:
        if id_server['battlemetrics_id'] != '':
            await ctx.send(tools.get_status_servers(id_server['battlemetrics_id']))

@bot.command(name='get_dino_list', description='Pesquisa na base de dados os dinos disponiveis com base no termo de pesquisa')
async def _dino_list(ctx, dino_name):
    """Pesquisa dinos disponiveis para desova"""
    print(">> Consulta a lista de dinos executada _dino_list_ param: " + dino_name)
    await ctx.send('Querying data, please wait..')
    x = rcon_console.patreon_dino_option(dino_name)
    await ctx.send(x)

@bot.command(name='locate_player', description='Find player on cluster maps and return gps map and location')
async def _locate_player(ctx, member:discord.Member):
    id_guild = '517617870612725763'

    try:
        id64_steam_info = rcon_console.get_id64_steam(member.id)
        id64_steam = id64_steam_info[0]['id_steam']
    except:
    #if id64_steam == None or id64_steam == '':
        await ctx.send('Player id64 ' + member.name + ' not found, player registration required to use this command')
        return

    server_id = rcon_console.get_user_active_server(id_guild, id64_steam)

    if server_id > 0:
        server_info = rcon_console.get_server_info(id_guild, server_id)
        if server_info != None:
            gps_player = rcon_console.get_player_pos_gps(id_guild,id64_steam,server_id)
            if server_info['description'] != None:
                description_server = ' - ' + server_info['description']
            else:
                description_server = ' - '
            msg = 'Player is active on map ' + server_info['map_name'] + description_server + ' | pos. ' + gps_player
        else:
            msg = 'Player not found :('
        
        await ctx.send(msg)

@bot.command(description='Admin command spawn for player location')
async def admin_spwan_dino(ctx, member:discord.Member, id_dino):
    id64_steam_info = rcon_console.get_id64_steam(member.id)
    id64_steam = id64_steam_info[0]['id_steam']

    if id64_steam != None:
        msg = spwan_dino(ctx, id64_steam, id_dino)
    else:
        msg = 'Id64 user not found, please register id64 for use this command'
    await ctx.send(msg)

@bot.command(name='get_patreon_dino')
async def spwan_my_dino(ctx, id_dino):
    """Spawn dino in player location """
    
    id64_steam_info = rcon_console.get_id64_steam(ctx.author.id)
    id64_steam = id64_steam_info[0]['id_steam']
    if id64_steam != None:
        msg = spwan_dino( ctx, id64_steam, id_dino)
    else:
        msg = 'Id64 user not found, please register id64 for use this command'
    await ctx.send(msg)

def spwan_dino(ctx, id64_steam,  id_dino_spwan):
    """Desova o dino escolhido proximo ao jogador"""
    
    #await ctx.send('Resource still under development, being released for use in the near future')
    #return
    id_guild = '517617870612725763'
    print(">> Comando de desova executado _dino_spawn_ param: " + str(id_dino_spwan))
    if id_dino_spwan != '':
        id_map_server = rcon_console.get_user_active_server(id_guild, id64_steam)
        pos_user = rcon_console.get_player_pos_absolute(id_guild, id64_steam, id_map_server)
        if id_map_server != '':
            # consulta o comando de spawn no banco de dados
            cmd_spwan_info = rcon_console.get_command_spwan(id_dino_spwan)
            cmd_spwan = cmd_spwan_info['blueprint_path']
            if cmd_spwan != '':
                # Consulta o level máximo definido para a guilda
                max_level = rcon_console.get_max_level_spwan(id_guild)
                if max_level != '':
                    # executando o comando de spawn no servidor via Rcon
                    msg = rcon_console.spwan_dino(id_guild, id_map_server, id64_steam, cmd_spwan, max_level, pos_user)
                    msg = msg + ' | Name: ' + cmd_spwan_info['id_name']
                else:
                    msg = 'Max level not registred'
            else:
                msg = 'id_spawn not found'
        else:
            msg = 'User not found in map'
    else:
        msg = 'Parâmetros incorretos'

    return msg

if __name__ == '__main__':
    keep_alive.keep_alive()
    token = os.environ.get('TOKEN_DISCORD')
    bot.run(token, bot=True, reconnect=True)