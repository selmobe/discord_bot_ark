from rcon           import select_data, insert_data
from _utils           import converter_localizacao_gps
import json
import factorio_rcon

rcon = factorio_rcon
rcon_port = 0
rcon_host = ''
rcon_pwd = ''
rcon_map = ''

def register_idsteam(name_discord, id_steam, id_discord):
    msg = insert_data.set_id64_steam(name_discord, str(id_steam), str(id_discord))
    return msg

def broadcast_all_servers(p_id_guilda, p_message):

    json_file = select_data.get_guild_servers(p_id_guilda)
    for row in json_file:
        rcon_host = row['ip_server']
        rcon_port = int(row['rcon_port'])
        rcon_pwd = row['rcon_password']
        try:
            cliente = rcon.RCONClient(rcon_host, rcon_port, rcon_pwd)
            command_rcon = cliente.send_command('broadcast  ' + p_message)
        except:
            print('Error: ' + command_rcon)

            
def get_player_pos_gps(p_id_guilda, p_id_player, p_id_server):

    json_file = select_data.get_guild_servers(p_id_guilda)
    rcon_status = False

    for row in json_file:
        if row['id_server_sk'] == int(p_id_server):
            rcon_host = row['ip_server']
            rcon_port = int(row['rcon_port'])
            rcon_pwd = row['rcon_password']
            rcon_map = row['map_name']
            rcon_status = True
            break

    if rcon_status == True:
        #DEFINE OS PARÂMETROS PARA A CONEXÃO AO SERVIDOR VIA RCON
        cliente = rcon.RCONClient(rcon_host, rcon_port, rcon_pwd)

        #ENVIA O COMANDO DE LOCALIZAÇÃO PARA O CONSOLE RCON 
        posicao = cliente.send_command('getplayerpos ' + p_id_player)

        if posicao =="Can't find player from the given steam id":
            return 'O jogador não está ativo neste momento no mapa definido!'

        #CONVERTE AS COORDENADAS PARA GPS
        r_gps = converter_localizacao_gps.coordenadas_em_gps(posicao, rcon_map)

        posicao_gps = 'Lat.: ' + str(r_gps[0]) + ' - Long.: ' + str(r_gps[1])
        return posicao_gps
    else:
        return 'Não foi localizado o servidor solicitado!'

def get_player_pos_absolute(p_id_guilda, p_id_player, p_id_server):

    json_file = select_data.get_guild_servers(p_id_guilda)
    rcon_status = False

    for row in json_file:
        if row['id_server_sk'] == int(p_id_server):
            rcon_host = row['ip_server']
            rcon_port = int(row['rcon_port'])
            rcon_pwd = row['rcon_password']
            rcon_status = True
            break

    if rcon_status == True:
        #DEFINE OS PARÂMETROS PARA A CONEXÃO AO SERVIDOR VIA RCON
        cliente = rcon.RCONClient(rcon_host, rcon_port, rcon_pwd)

        #ENVIA O COMANDO DE LOCALIZAÇÃO PARA O CONSOLE RCON 
        posicao = cliente.send_command('getplayerpos ' + p_id_player)

        if posicao =="Can't find player from the given steam id":
            return 'O jogador não está ativo neste momento no mapa definido!'
        elif posicao == "Server received, But no response!!":
            return 'Servidor recebeu, mas não respondeu a solicitação'
        else:
            pos = posicao.split()
            x = pos[0]
            y = pos[1]
            z = pos[2]
            posicao = x[2:] + ' ' + y[2:] + ' ' + z[2:]

        return posicao
    else:
        return 'Não foi localizado o servidor solicitado!'

def get_players_online(p_id_guilda):

    json_file = select_data.get_guild_servers(p_id_guilda)
    
    if json_file == 'Não foi possivel recuperar os dados, servidor possivelmente não cadastrado':
        return "``` Servidor com dados invalidos cadastrado ou incompleto ```"

    server_list = []
    #css_mensagem = '```\n'
    for x in json_file:

        rcon_host = x['ip_server']
        rcon_port = int(x['rcon_port'])
        rcon_pwd = x['rcon_password']
        map_name = x['map_name']
        
        if x['description'] != None:
            description_server = ' - ' + x['description']
        else:
            description_server = ''
        #css_mensagem = css_mensagem + x['name_guild'] +' - ' + x['map_name'] + '\n###### Players Online  ##### \n'

        try:
            cliente = rcon.RCONClient(rcon_host, rcon_port, rcon_pwd)
            list_players = cliente.send_command('listplayers')
            if list_players=='No Players Connected':
                list_players = '\n0 - No Players Connected \n'
            list_players = list_players.replace(', 7',' - id64: 7')
        except:
            list_players = '\nNão foi possivel conectar ao servidor \n'
        
        server_list.append([map_name + description_server, [list_players]])
    #css_mensagem = css_mensagem +  '\n```'
    return server_list

def get_list_servers(p_id_guilda):
    """Recupera do servidor a lista de servidores associados a guilda consultada"""
    server_list = select_data.get_guild_servers(p_id_guilda)
    #css_mensagem = '```css\n####### SERVERS ################'
    list_server = []
    for server in server_list:
        if server['description'] != None:
            description_server = server['description']
        else:
            description_server = ''
        return_data = '\n### Id Server: ' + str(server['id_server_sk']) + ' - ' + server['name_guild'] + '\n###      Map: ' + server['map_name'] + '\n###      Modo: ' + server['mode_server'] + '\n###   Patreon: ' + server['map_patreon'] +  '\n###   Description: ' + description_server + '\n -----------------------------------------------------------------------------------'
        list_server.append(return_data)
        #css_mensagem = css_mensagem + return_data
    #css_mensagem = css_mensagem +  '\n##############################```'
    return list_server #css_mensagem

def get_server_info(p_id_guilda, p_id_server):
    """Recupera do servidor a lista de servidores associados a guilda consultada"""
    server_list = select_data.get_guild_servers(p_id_guilda)
 
    for server in server_list:
        if server['id_server_sk'] == p_id_server:
            return_data = server
            break
    return return_data 

def get_status_servers(p_id_guilda):
    """Utilizando o teste de porta para verificar disponibilidade do servidor"""
    json_file = select_data.get_guild_servers(p_id_guilda)
    css_mensagem = '```css\n'
    mensagem = ''

    for x in json_file:

        rcon_host = x['ip_server']
        rcon_port = int(x['rcon_port'])
        rcon_pwd = x['rcon_password']

        mensagem = mensagem + '\n### Id Server: ' + str(x['id_server_sk']) + ' - ' + x['name_guild'] + '\n###      Mapa: ' + x['map_name'] + '\n###      Modo: ' + x['mode_server'] + '\n###   Patreon: ' + x['map_patreon'] 

        try:
            rcon.RCONClient(rcon_host, rcon_port, rcon_pwd)
            mensagem = mensagem  + '\n###    Status: Online' + '\n### IP Server: ' + x['ip_server'] + '\n -----------------------------------------------------------------------------------' + '\n'
            
        except:
            mensagem = mensagem  + '\n###    Status: ::Offline' + '\n### IP Server: ' + x['ip_server'] + '\n -----------------------------------------------------------------------------------' + '\n' 
            pass
        
    
    css_mensagem = css_mensagem +  mensagem + '\n ```'
    return css_mensagem

def patreon_dino_option(dino_name):

    dino_list = select_data.get_list_dino(dino_name)

    if len(dino_list) >= 1:
        message_list = "```\n----------------- Options Spawn -----------------------\n"
        for x in dino_list:
            message_list = message_list + " ID_SPAWN: " + str(x['id_dino']) + " | "
            message_list = message_list + " ID NAME: " + str(x['id_name']) + " | "
            message_list = message_list + " CATEGORY: " + str(x['category']) + " | "
            message_list = message_list + " DINO TAG: " + str(x['dino_name_tag']) + " | \n"

        message_list = message_list + "```"
    else:
        message_list = 'Dino Not Found Match'
    return message_list

def get_command_spwan(id_dino):
    json_file = select_data.get_spawn_command(id_dino)
    x= json_file[0]
    return x

def get_max_level_spwan(p_id_guilda):
    json_file = select_data.get_spawn_max_level(p_id_guilda)
    x = json_file[0]
    return x['max_level']

def get_id64_steam(p_id64_steam):
    json_file = select_data.get_id_steam(p_id64_steam)
    return json_file

def spwan_dino(p_id_guilda, p_id_server, p_id64_steam, p_blueprint, p_max_level, p_user_pos):
    status = ''
    json_file = select_data.get_guild_servers(p_id_guilda)
    rcon_status = False

    for row in json_file:

        if row['id_server_sk'] == int(p_id_server):
            rcon_host = row['ip_server']
            rcon_port = int(row['rcon_port'])
            rcon_pwd = row['rcon_password']
            rcon_status = True

    if rcon_status == True:
        #DEFINE OS PARÂMETROS PARA A CONEXÃO AO SERVIDOR VIA RCON
        cliente = rcon.RCONClient(rcon_host, rcon_port, rcon_pwd)

        #ENVIA O COMANDO DE LOCALIZAÇÃO PARA O CONSOLE RCON 
        command_rcon = 'SpawnDino ' + str(p_id64_steam) + ' ' + p_blueprint + ' ' + str(p_max_level) + ' ' + str(1) + ' ' + p_user_pos

        try:
            status = cliente.send_command(command_rcon)
            status = status + ' in location ' +  get_player_pos_gps(p_id_guilda, p_id64_steam, p_id_server)
        except:
            print('Algo erro não esta certo, spawn não realizado')
            return 'Error: Please check the admin channel for more info'

        finally:
            print(status)
            return status

def get_user_active_server(p_id_guilda, p_id64_steam):
    server_list = select_data.get_guild_servers(p_id_guilda)

    for x in server_list:
        user_pos = get_player_pos_absolute(p_id_guilda, p_id64_steam, x['id_server_sk'])
        if user_pos != '' and user_pos != 'O jogador não está ativo neste momento no mapa definido!' and user_pos != 'Servidor recebeu, mas não respondeu a solicitação':
            return x['id_server_sk']
    return 'O jogador não está ativo neste momento no mapa definido!'
        
if __name__ == '__main__':
    print(get_user_active_server('609915604392083466', '76561198891523532'))
