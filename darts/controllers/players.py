from darts import app
from flask import Blueprint, request, render_template, redirect
from darts.entities import player as playerModel, game as gameModel, team_player as teamPlayerModel, score as scoreModel
from darts import model

mod = Blueprint("players", __name__, url_prefix = "/players")

@mod.route("/", methods = ["GET"])
def players_index():
	players = model.Model().select(playerModel.Player)
	return render_template("players/index.html", players = players)

@mod.route("/new/", methods = ["GET"])
def players_new():
	return render_template("players/new.html")

@mod.route("/", methods = ["POST"])
def players_create():
	newPlayer = playerModel.Player(request.form["name"])
	model.Model().create(newPlayer)
	return redirect("/players/")

@mod.route("/<int:id>/", methods = ["GET"])
def players_details(id):
	player = model.Model().selectById(playerModel.Player, id)
	teams = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(playerId = id)
	scores = model.Model().select(scoreModel.Score).filter_by(playerId = id)
	return render_template("players/details.html", player = player, teams = teams, scores = scores)

@mod.route("/<int:id>/edit/", methods = ["GET"])
def players_edit(id):
	players = model.Model().selectById(playerModel.Player, id)
	return render_template("players/edit.html", player = players)

@mod.route("/<int:id>/", methods = ["POST"])
def players_update(id):
	model.Model().update(playerModel.Player, id, request.form)
	return redirect("/players/")

@mod.route("/<int:id>/delete/", methods = ["POST"])
def players_delete(id):
	model.Model().delete(playerModel.Player, id)
	return redirect("/players/")
