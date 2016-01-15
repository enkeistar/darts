from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Mode(Base):

	__tablename__ = "modes"

	id = Column(Integer, primary_key = True)
	name = Column(String)
	enabled = Column(Integer)

	def __init__(self, enabled):
		self.name = name
		self.enabled = enabled
