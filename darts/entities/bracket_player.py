from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BracketPlayer(Base):

	__tablename__ = "brackets_players"

	id = Column(Integer, primary_key = True)
	bracketId = Column(Integer)
	playerId = Column(Integer)

	def __init__(self, bracketId, playerId):
		self.bracketId = bracketId
		self.playerId = playerId
