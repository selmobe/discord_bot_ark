#coding=utf-8

from sqlalchemy import Column, String, Integer
from my_tables.base import Base

class MaxLevelSpawn(Base):
    __tablename__ = "tbl_max_level_spawn"
    __table_args__  =  {'schema':'discord_ark_bot'} 
    id            = Column(Integer, primary_key=True)
    guild_id      = Column(String(18), unique=True)
    max_level     = Column(Integer)

    def __init__(self, discord_name, id_steam):
        self.discord_name   = discord_name
        self.id_steam       = id_steam 