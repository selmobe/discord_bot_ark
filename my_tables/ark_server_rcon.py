#coding=utf-8

from sqlalchemy import Column, String, Integer
from my_tables.base import Base, schema

class ArkServerRcon(Base):
    __tablename__ = "tbl_ark_server"
    __table_args__  =  {'schema':schema} 

    id                = Column(Integer, primary_key=True)
    id_guild          = Column(String(18))
    ip_server         = Column(String(15))
    rcon_port         = Column(Integer)
    rcon_password     = Column(String(100))
    id_server_sk      = Column(Integer)
    mode_server       = Column(String(3))
    map_name          = Column(String(50))
    map_patreon       = Column(String(3))
    battlemetrics_id  = Column(String(10), nullable=True)
    description       = Column(String(200), nullable=True)

    def __init__(self, id_guild, ip_server, rcon_port, rcon_password, id_server_sk, mode_server, map_name, map_patreon, battlemetrics_id, description):
        self.id_guild           = id_guild
        self.ip_server          = ip_server
        self.rcon_port          = rcon_port
        self.rcon_password      = rcon_password
        self.id_server_sk       = id_server_sk
        self.mode_server        = mode_server
        self.map_name           = map_name
        self.map_patreon        = map_patreon 
        self.battlemetrics_id   = battlemetrics_id
        self.description        = description