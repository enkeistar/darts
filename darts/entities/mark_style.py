from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MarkStyle(Base):

	__tablename__ = "mark_styles"

	id = Column(Integer, primary_key = True)
	one = Column(String)
	two = Column(String)
	three = Column(String)
	approved = Column(Integer)
	createdAt = Column(DateTime)

	def __init__(self, one, two, three, approved, createdAt):
		self.one = one
		self.two = two
		self.three = three
		self.approved = approved
		self.createdAt = createdAt
