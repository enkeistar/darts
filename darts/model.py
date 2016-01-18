from darts import app
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import json

app.config["MYSQL_USERNAME"] = ""
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_HOST"] = ""
app.config["MYSQL_DATABASE"] = ""

app.config.from_pyfile("config_file.cfg")

engine = create_engine("mysql+mysqldb://" + app.config["MYSQL_USERNAME"] + ":" + app.config["MYSQL_PASSWORD"] + "@" + app.config["MYSQL_HOST"] + "/" + app.config["MYSQL_DATABASE"])
db_session = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = engine))
Session = sessionmaker(bind = engine)
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

	def getSession(self):
		return session
