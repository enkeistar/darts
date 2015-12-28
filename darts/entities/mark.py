from sqlalchemy import create_engine, Column, Integer, DateTime, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Mark(Base):

	__tablename__ = "marks"

	id = Column(Integer, primary_key = True)
	gameId = Column(Integer)
	teamId = Column(Integer)
	playerId = Column(Integer)
	game = Column(Integer)
	round = Column(Integer)
	twenty = Column(TINYINT, default = 0)
	nineteen = Column(TINYINT, default = 0)
	eighteen = Column(TINYINT, default = 0)
	seventeen = Column(TINYINT, default = 0)
	sixteen = Column(TINYINT, default = 0)
	fifteen = Column(TINYINT, default = 0)
	bullseye = Column(TINYINT, default = 0)
	createdAt = Column(DateTime)
