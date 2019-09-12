#coding=utf-8

from sqlalchemy import Column, String, Integer
from my_tables.base import Base

class Id64Steam(Base):
    __tablename__ = "tbl_id_steam"
    __table_args__  =  {'schema':'discord_ark_bot'} 
    id            = Column(Integer, primary_key=True)
    discord_name  = Column(String(100), unique=True)
    id_steam      = Column(String(20))
    id_discord    = Column(String(20))

    def __init__(self, discord_name, id_steam, id_discord):
        self.discord_name   = discord_name
        self.id_steam       = id_steam 
        self.id_discord     = id_discord