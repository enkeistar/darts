from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TeamPlayer(Base):

	__tablename__ = "teams_players"

	id = Column(Integer, primary_key = True)
	teamId = Column(Integer)
	playerId = Column(Integer)

	def __init__(self, teamId, playerId):
		self.teamId = teamId
		self.playerId = playerId
