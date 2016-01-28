from darts import app
from flask import request, render_template, redirect
from darts.entities import player as playerModel
from darts.entities import game as gameModel
from darts.entities import team as teamModel
from darts.entities import team_player as teamPlayerModel
from darts.entities import mark as markModel
from darts import model
from datetime import datetime
from sqlalchemy import distinct

@app.route("/players/", methods = ["GET"])
def players_index():
	players = model.Model().select(playerModel.Player).order_by(playerModel.Player.name)
	return render_template("players/index.html", players = players)

@app.route("/players/new/", methods = ["GET"])
def players_new():
	return render_template("players/new.html", gameId = 0, name = "", error = False)

@app.route("/players/games/<int:gameId>/new/", methods = ["GET"])
def players_new_game(gameId):
	return render_template("players/new.html", gameId = gameId)

@app.route("/players/", methods = ["POST"])
def players_create():

	gameId = int(request.form["gameId"])

	players = model.Model().select(playerModel.Player).filter_by(name = request.form["name"])

	if players.count() > 0:
		return render_template("players/new.html", gameId = gameId, name = request.form["name"], error = True)

	newPlayer = playerModel.Player(request.form["name"], datetime.now())
	model.Model().create(newPlayer)

	if gameId == 0:
		return redirect("/players/")
	else:
		return redirect("/games/" + str(gameId) + "/modes/cricket/players/")

@app.route("/players/<int:id>/", methods = ["GET"])
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

@app.route("/players/<int:id>/edit/", methods = ["GET"])
def players_edit(id):
	player = model.Model().selectById(playerModel.Player, id)
	return render_template("players/edit.html", player = player, error = False)

@app.route("/players/<int:id>/", methods = ["POST"])
def players_update(id):
	players = model.Model().select(playerModel.Player).filter_by(name = request.form["name"]).filter(playerModel.Player.id != id)

	if players.count() > 0:
		player = model.Model().selectById(playerModel.Player, id)
		player.name = request.form["name"]
		return render_template("players/edit.html", player = player, error = True)

	model.Model().update(playerModel.Player, id, request.form)
	return redirect("/players/")

@app.route("/players/<int:id>/delete/", methods = ["POST"])
def players_delete(id):
	model.Model().delete(playerModel.Player, id)
	return redirect("/players/")


