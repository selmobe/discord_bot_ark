from sqlalchemy                     import exc
from sqlalchemy                     import MetaData
from my_tables.base                 import Session, engine, Base
from my_tables.id64_steam           import Id64Steam
from my_tables.discord_guild        import DiscordGuild
from my_tables.ark_server_rcon      import ArkServerRcon
from rcon                           import select_data

Base.metadata.create_all(engine)
#meta = MetaData(engine, reflect=True)

def commit_session(insert_data):
    """Executa o comando de INSERT realizando a tratativa do erro se necessário"""
    try:
        session = Session()
        session.add(insert_data)
        session.commit()
        return_commit = "successfully"
    except exc.SQLAlchemyError:
        return_commit = "error"
    finally:
        session.close()
    return return_commit
    
def set_id64_steam(p_discord_name,  p_id64_steam, p_id_discord):
    if p_discord_name != '' and p_id64_steam != '':
        insert_data = Id64Steam(p_discord_name, p_id64_steam, p_id_discord)
        return commit_session(insert_data)
    else:
        return 'Campos em branco, dados não inseridos'

def set_register_server_ark(p_discord_id_guild,  p_ip_server, p_rcon_port, p_rcon_password, p_server_mode, p_map_name, p_map_patreon, p_description):
    if p_discord_id_guild != '' and p_ip_server != '' and p_rcon_port != '' and p_rcon_password != '' and p_server_mode != '' and p_map_patreon != '':
        count_servers = select_data.get_count_server_guild(p_discord_id_guild)
        insert_data = ArkServerRcon(p_discord_id_guild, p_ip_server, p_rcon_port, p_rcon_password, (count_servers + 1), p_server_mode, p_map_name, p_map_patreon, '', p_description)
        
        return commit_session(insert_data)
    else:
        return 'Campos em branco, dados não inseridos'

def set_register_guild(p_id_guild, p_guild_name):
    """Registra no banco de dados o id e nome da guilda"""
    if p_id_guild != '' and p_guild_name != '':
        insert_data = DiscordGuild(p_id_guild, p_guild_name)
        return commit_session(insert_data)
    else:
        return 'Campos em branco, dados não gravados'

def set_unregister_guild(p_id_guild):
    """Remove do banco de dados a guilda definida"""
    try:
        session = Session()
        delete_data = session.query(DiscordGuild).filter(DiscordGuild.id_guild == str(p_id_guild)).first()
        session.delete(delete_data)
        session.commit()
        msg_return = 'successfully'

    except exc.SQLAlchemyError:
        msg_return =  'Erro ao deletar o registro do DB'

    finally:
        session.close() 

    return msg_return
 


