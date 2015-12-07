from darts import app
from flask import Blueprint, Response, request, render_template, redirect
from darts.entities import player
from darts import model
import json

mod = Blueprint("players", __name__, url_prefix = "/players")

@mod.route("/", methods = ["GET"])
def players_index():
	players = model.Model().select(player.Player)
	return render_template("players/index.html", players = players)

@mod.route("/new/", methods = ["GET"])
def players_new():
	return render_template("players/new.html")

@mod.route("/", methods = ["POST"])
def players_create():
	newPlayer = player.Player(request.form["name"])
	model.Model().create(newPlayer)
	return redirect("/players/")

@mod.route("/<int:id>/", methods = ["GET"])
def players_details(id):
	return "details"

@mod.route("/<int:id>/edit/", methods = ["GET"])
def players_edit(id):
	players = model.Model().selectById(player.Player, id)
	return render_template("players/edit.html", player = players)

@mod.route("/<int:id>/", methods = ["POST"])
def players_update(id):
	model.Model().update(player.Player, id, request.form)
	return redirect("/players/")

@mod.route("/<int:id>/delete/", methods = ["POST"])
def players_delete(id):
	model.Model().delete(player.Player, id)
	return redirect("/players/")


