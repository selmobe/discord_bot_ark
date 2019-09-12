#coding=utf-8
from sqlalchemy import Column, String, Integer
from my_tables.base import Base, schema

class SpwanDinoCommand(Base):
    __tablename__ = "tbl_spawn_dino_command"
    __table_args__  =  {'schema':schema} 
    id_dino        = Column(Integer, primary_key = True)
    id_name        = Column(String(50))
    category       = Column(String(50))
    dino_name_tag  = Column(String(50))
    entity_id      = Column(String(50))
    blueprint_path = Column(String(200))

    def __init__(self, id_dino, id_name, category, dino_name_tag, entity_id, blueprint_path):
        self.id_dino        = id_dino
        self.id_name        = id_name
        self.category       = category
        self.dino_name_tag  = dino_name_tag
        self.entity_id      = entity_id
        self.blueprint_path = blueprint_path