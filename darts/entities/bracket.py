from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bracket(Base):

	__tablename__ = "brackets"

	id = Column(Integer, primary_key = True)
	players = Column(Integer)
	bracketType = Column(String)
	createdAt = Column(DateTime)

	def __init__(self, players, bracketType, createdAt):
		self.players = players
		self.bracketType = bracketType
		self.createdAt = createdAt
