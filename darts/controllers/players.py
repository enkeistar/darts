from darts import app
from flask import Blueprint, request, render_template, redirect
from darts.entities import player as playerModel, game as gameModel, team as teamModel, team_player as teamPlayerModel, mark as markModel
from darts import model
from datetime import datetime
from sqlalchemy import distinct

mod = Blueprint("players", __name__, url_prefix = "/players")

@mod.route("/", methods = ["GET"])
def players_index():
	players = model.Model().select(playerModel.Player).order_by(playerModel.Player.name)
	return render_template("players/index.html", players = players)

@mod.route("/new/", methods = ["GET"])
def players_new():
	return render_template("players/new.html", gameId = 0)

@mod.route("/games/<int:gameId>/new/", methods = ["GET"])
def players_new_game(gameId):
	return render_template("players/new.html", gameId = gameId)

@mod.route("/", methods = ["POST"])
def players_create():
	newPlayer = playerModel.Player(request.form["name"], datetime.now())
	model.Model().create(newPlayer)

	gameId = request.form["gameId"]

	if gameId == "0":
		return redirect("/players/")
	else:
		return redirect("/games/" + str(gameId) + "/players/")

@mod.route("/<int:id>/", methods = ["GET"])
def players_details(id):
	player = model.Model().selectById(playerModel.Player, id)
	teamPlayers = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(playerId = id)
	marks = model.Model().select(markModel.Mark).filter_by(playerId = id)

	session = model.Model().getSession()
	query = session.query(markModel.Mark.gameId, markModel.Mark.teamId, markModel.Mark.game, markModel.Mark.round).filter_by(playerId = id)
	query = query.distinct(markModel.Mark.gameId)
	query = query.distinct(markModel.Mark.teamId)
	query = query.distinct(markModel.Mark.round)
	query = query.distinct(markModel.Mark.game)
	rounds = len(query.all())

	teamIds = []
	for teamPlayer in teamPlayers:
		teamIds.append(teamPlayer.teamId)

	teams = model.Model().select(teamModel.Team).filter(teamModel.Team.id.in_(teamIds))

	wins = teams.filter_by(win = 1).count()
	losses = teams.filter_by(loss = 1).count()

	points = 0

	game = 0
	round = 0
	for mark in marks:
		if game != mark.gameId and round != mark.round:
			scored = {
				20: 0,
				19: 0,
				18: 0,
				17: 0,
				16: 0,
				15: 0,
				25: 0,
				0: 0
			}
			game = mark.gameId
			round = mark.round

		scored[mark.value] += 1
		if scored[mark.value] > 3:
			points += mark.value

	return render_template("players/details.html", player = player, teamPlayers = teamPlayers, marks = marks, wins = wins, losses = losses, points = points, rounds = rounds)

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
