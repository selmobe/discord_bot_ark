#coding=utf-8

from sqlalchemy import Column, String, Integer
from my_tables.base import Base, schema

class DiscordGuild(Base):
    __tablename__   = "tbl_discord_guild"
    __table_args__  =  {'schema':schema} #{'schema':'discord_ark_bot'} 
    id                = Column(Integer, primary_key=True)
    id_guild          = Column(String(18), unique=True)
    name_guild        = Column(String(150))

    def __init__(self, id_guild, name_guild):
        self.id_guild   = id_guild
        self.name_guild = name_guild