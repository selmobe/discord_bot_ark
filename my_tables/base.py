# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

_db_user = os.environ.get('POSTGRESQL_USUARIO')
_db_password = os.environ.get('POSTGRESQL_SENHA')
_db_host = os.environ.get('POSTGRESQL_HOST')
_db_port = os.environ.get('POSTGRESQL_PORTA')
_db_database = os.environ.get('POSTGRESQL_BASEDEDADOS')

_url_connection = 'postgresql://' + _db_user + ':' + _db_password + '@' + _db_host + ':' + _db_port + '/' + _db_database

engine = create_engine(_url_connection)

Session = sessionmaker(bind=engine)
schema = 'discord_ark_bot'
Base = declarative_base()