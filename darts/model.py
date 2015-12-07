from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import json

engine = create_engine("mysql+mysqldb://brett:r45ftthry@localhost/darts")
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind = engine))
Session = sessionmaker(bind=engine)
session = Session()

class Model():

	def select(self, model):
		return session.query(model)

	def selectById(self, model, id):
		return session.query(model).filter(model.id == id).one()

	def create(self, data):
		session.add(data)
		session.commit()
		return data

	def update(self, model, id, data):
		session.query(model).filter(model.id == id).update(data)
		session.commit()
		return data

	def delete(self, model, id):
		session.query(model).filter(model.id == id).delete()
		session.commit()
