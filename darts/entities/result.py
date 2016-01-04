from sqlalchemy import create_engine, Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

class Result(Base):

	__tablename__ = "results"

	id = Column(Integer, primary_key = True)
	gameId = Column(Integer)
	teamId = Column(Integer)
	game = Column(Integer)
	score = Column(Integer)
	win = Column(Integer)
	loss = Column(Integer)
	createdAt = Column(DateTime)

	def __init__(self, gameId, teamId, game, score, win, loss, createdAt):
		self.gameId = gameId
		self.teamId = teamId
		self.game = game
		self.score = score
		self.win = win
		self.loss = loss
		self.createdAt = createdAt
