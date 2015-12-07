from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


Base = declarative_base()

class User(Base):

	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	firstName = Column(String)
	lastName = Column(String)

	def __init__(self, firstName, lastName):
		self.firstName = firstName
		self.lastName = lastName
