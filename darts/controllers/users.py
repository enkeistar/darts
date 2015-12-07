from darts import app
from flask import Blueprint, Response, request
from darts.entities import user
from darts import model
import json

mod = Blueprint("users", __name__, url_prefix = "/users")

@mod.route("/", methods = ["GET"])
def users_index():
	data = model.Model()
	result = data.select(user.User)
	return Response(data.toJson(result), mimetype = "application/json")


@mod.route("/", methods = ["POST"])
def users_create():
	data = model.Model()
	newUser = user.User(request.form["firstName"], request.form["lastName"])
	data.save(newUser)
	# return json.dumps({ "id": str(newUser.id), "firstName": newUser.firstName, "lastName": newUser.lastName })
	# return str({ "id": str(newUser.id), "firstName": newUser.firstName, "lastName": newUser.lastName })
	return Response(json.dumps({ "id": str(newUser.id), "firstName": newUser.firstName, "lastName": newUser.lastName }), status = 200, mimetype = "application/json")
