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

class Model():

	def select(self, model):
		session = Session()
		data = session.query(model)
		session.close()
		return data

	def selectById(self, model, id):
		session = Session()
		data = session.query(model).filter(model.id == id).one()
		session.close()
		return data

	def create(self, data):
		session = Session()
		session.add(data)
		session.commit()
		session.close()
		return data

	def update(self, model, id, data):
		session = Session()
		session.query(model).filter(model.id == id).update(data)
		session.commit()
		session.close()
		return data

	def delete(self, model, id):
		session = Session()
		session.query(model).filter(model.id == id).delete()
		session.commit()
		session.close()

	def getSession(self):
		return Session()
