from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

class Player(Base):

	__tablename__ = "players"

	id = Column(Integer, primary_key = True)
	name = Column(String)

	def __init__(self, name):
		self.name = name
