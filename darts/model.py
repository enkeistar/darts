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
		result = session.query(model)
		return result

	def save(self, data):
		session.add(data)
		session.commit()
		return data

	def toJson(self, data):
		list = []

		for row in data:
			list.append({ "id": row.id, "firstName": row.firstName, "lastName": row.lastName })

		return json.dumps(list)
