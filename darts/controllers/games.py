from darts import app
from flask import Blueprint, render_template, redirect, request
from darts.entities import game as gameModel, player as playerModel, team as teamModel, team_player as teamPlayerModel, score as scoreModel
from darts import model
from datetime import datetime

import pprint

mod = Blueprint("games", __name__, url_prefix = "/games")

@mod.route("/<int:id>/", methods = ["GET"])
def games_index(id):
	game = model.Model().selectById(gameModel.Game, id)
	teams = model.Model().select(teamModel.Team).filter_by(gameId = game.id)

	data = {
		"id": int(game.id),
		"teams": []
	}

	for team in teams:

		newTeam = {
			"id": team.id,
			"players": []
		}

		players = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(teamId = team.id)

		for player in players:

			user = model.Model().selectById(playerModel.Player, int(player.playerId))

			newTeam["players"].append({
				"id": int(user.id),
				"name": user.name
			})

		data["teams"].append(newTeam)

	return render_template("games/index.html", game = data)

@mod.route("/new/", methods = ["GET"])
def games_new():
	return render_template("games/new.html")

@mod.route("/", methods = ["POST"])
def games_create():
	newGame = gameModel.Game(request.form["players"], datetime.now())
	model.Model().create(newGame)
	return redirect("/games/%d/players/" % newGame.id)

@mod.route("/<int:id>/players/", methods = ["GET"])
def games_players(id):
	game = model.Model().selectById(gameModel.Game, id)
	players = model.Model().select(playerModel.Player)
	return render_template("games/players.html", players = players, game = game)

@mod.route("/<int:id>/", methods = ["POST"])
def games_start(id):
	game = model.Model().selectById(gameModel.Game, id)

	newTeam1 = teamModel.Team(id);
	model.Model().create(newTeam1)

	newTeam2 = teamModel.Team(id);
	model.Model().create(newTeam2)

	team1Player1 = teamPlayerModel.TeamPlayer(newTeam1.id, request.form["team-1-player-1-id"]);
	model.Model().create(team1Player1)

	team2Player1 = teamPlayerModel.TeamPlayer(newTeam2.id, request.form["team-2-player-1-id"]);
	model.Model().create(team2Player1)

	if game.players == 4:
		team1Player2 = teamPlayerModel.TeamPlayer(newTeam1.id, request.form["team-1-player-2-id"]);
		model.Model().create(team1Player2)

		team2Player2 = teamPlayerModel.TeamPlayer(newTeam2.id, request.form["team-2-player-2-id"]);
		model.Model().create(team2Player2)

	return redirect("/games/%d/" % id)

@mod.route("/<int:id>/score", methods = ["POST"])
def games_score(id):

	newScore = scoreModel.Score()
	newScore.gameId = id
	newScore.teamId = request.form["teamId"]
	newScore.playerId = request.form["playerId"]
	newScore.round = request.form["round"]
	newScore.createdAt = datetime.now()

	points = int(request.form["points"])

	if points == 20:
		newScore.twenty = 1
	elif points == 19:
		newScore.nineteen = 1
	elif points == 18:
		newScore.eighteen = 1
	elif points == 17:
		newScore.seventeen = 1
	elif points == 16:
		newScore.sixteen = 1
	elif points == 15:
		newScore.fifteen = 1
	elif points == 25:
		newScore.bullseye = 1

	model.Model().create(newScore)

	return str({
		"id": int(newScore.id)
	})