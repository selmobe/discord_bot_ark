from sqlalchemy                     import exc, desc
from my_tables.base                 import Session
from my_tables.discord_guild        import DiscordGuild
from my_tables.spawn_dino_command   import SpwanDinoCommand
from my_tables.max_level_spawn      import MaxLevelSpawn
from my_tables.id64_steam           import Id64Steam
from my_tables.ark_server_rcon      import ArkServerRcon
from sqlalchemy                     import inspect
import json



def get_guild_servers(p_id_guild):
    """ Recupera do banco de dados os servidores associado a guilda do Discord"""
    try:
        session = Session()
        select_data = session.query(DiscordGuild.name_guild, ArkServerRcon.ip_server, ArkServerRcon.rcon_password,
                                                            ArkServerRcon.rcon_port,
                                                            ArkServerRcon.id_server_sk,
                                                            ArkServerRcon.mode_server,
                                                            ArkServerRcon.map_name,
                                                            ArkServerRcon.battlemetrics_id,
                                                            ArkServerRcon.map_patreon, 
                                                            ArkServerRcon.description)\
        .filter(DiscordGuild.id_guild == ArkServerRcon.id_guild)\
        .filter(ArkServerRcon.id_guild == str(p_id_guild))\
        .order_by(desc(ArkServerRcon.id_server_sk))\
        .all()
    except exc.SQLAlchemyError:
        print(" Erro ao consultar os dados")
    finally:
        session.close()

    if len(select_data) == 0:
        session.close()
        return 'Não foi possivel recuperar os dados, servidor possivelmente não cadastrado'
    else:
        session.close()
        return table_to_json(select_data)

def get_list_dino(p_dino_name):
    """ Recupera do servidor uma consulta tendo como parâmetro o nome do dino """
    try:
        session = Session()
        select_data = session.query(SpwanDinoCommand.id_dino, SpwanDinoCommand.id_name, SpwanDinoCommand.category, SpwanDinoCommand.dino_name_tag, SpwanDinoCommand.entity_id, SpwanDinoCommand.blueprint_path)\
                .filter(SpwanDinoCommand.id_name.ilike('%' + p_dino_name + '%'))\
                .all()
        msg = table_to_json(select_data, SpwanDinoCommand)
    except exc.SQLAlchemyError:
        msg = 'Erro ao consutar tabela'
    finally:
        session.close()
    return msg

def get_count_server_guild(p_id_guild):
    """ Recupera do servidor a quantidade de servidores associados a guild """
    try:
        session = Session()
        select_data = session.query(ArkServerRcon)\
                .filter(ArkServerRcon.id_guild == str(p_id_guild))\
                .count()
                
        msg = select_data
    except exc.SQLAlchemyError:
        msg = 'Erro ao consutar tabela'
    finally:
        session.close()
    return msg
    
def get_count_server_register():
    """ Recupera do servidor a quantidade de servidores totais cadastrados """
    try:
        session = Session()
        select_data = session.query(ArkServerRcon)\
                .count()

        msg = select_data
    except exc.SQLAlchemyError:
        msg = 'Erro ao consutar tabela'
    finally:
        session.close()
    return msg

def get_spawn_command(p_id_dino):
    """ Recupera do banco de dados os dados do dino"""
    try:
        session = Session()
        select_data = session.query(SpwanDinoCommand.id_dino, SpwanDinoCommand.id_name, SpwanDinoCommand.blueprint_path )\
            .filter(SpwanDinoCommand.id_dino == int(p_id_dino))\
            .all()
            
        msg = table_to_json(select_data, SpwanDinoCommand)
    except exc.SQLAlchemyError:
        print(" Erro ao consultar comando de Spawn")
        msg = 'Error'
    finally:
        session.close()
    return msg

def get_spawn_max_level(p_id_guild):
    """ Recupera do banco de dados o level máximo para desova para o servidor que realizou a consulta"""
    try:
        session = Session()
        select_data = session.query(MaxLevelSpawn.id, MaxLevelSpawn.guild_id, MaxLevelSpawn.max_level)\
            .filter(MaxLevelSpawn.guild_id == str(p_id_guild))\
            .all()
        msg = table_to_json(select_data, MaxLevelSpawn)
    except exc.SQLAlchemyError:
        print(" Erro ao consultar os dados")
        msg = 'Error'
    finally:
        session.close()
    return msg

def get_id_steam(p_id_discord):
    """ Recupera do servidor o id64 Steam associado ao id do usuário Discord"""
    try:
        session = Session()
        select_data = session.query(Id64Steam.id, Id64Steam.discord_name, Id64Steam.id_steam, Id64Steam.id_discord)\
            .filter(Id64Steam.id_discord == str(p_id_discord))\
            .all()
        msg = table_to_json(select_data, Id64Steam)
    except exc.SQLAlchemyError:
        print(" Erro ao consultar os dados")
        msg = 'Error'
    finally:
        session.close()
    return msg

def table_to_json(table_entry, obj_table = None):
    """ Converte a tabela de consulta em dados no formato Json"""    
    name_fields = []
    #if obj_table != None:
    #    mapper = inspect(obj_table)
    #    for column in mapper.attrs:
    #        name_fields.append(column.key)
    #else:
    for x in table_entry:
        for column in x._fields:
            name_fields.append(column)
        break
    
    table_exit = []
    for row in table_entry:
        table_exit.append(dict(zip(name_fields, row)))

    rem = json.dumps(table_exit)
    js_return = json.loads(rem)
    return js_return

if __name__ == '__main__':
    print(get_spawn_max_level('609915604392083466'))
    print(get_list_dino(200))