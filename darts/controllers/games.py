from darts import app
from flask import Blueprint, Response, render_template, redirect, request
from darts.entities import game as gameModel, player as playerModel, team as teamModel, team_player as teamPlayerModel, score as scoreModel
from darts import model
from datetime import datetime
from sqlalchemy import desc
import operator
import json

import pprint

mod = Blueprint("games", __name__, url_prefix = "/games")

@mod.route("/", methods = ["GET"])
def games_index():

	data = []

	games = model.Model().select(gameModel.Game).order_by(desc("createdAt"))

	for game in games:

		gameData = {
			"id": game.id,
			"date": "{:%b %d, %Y} ".format(game.createdAt),
			"time": "{:%I:%M %p}".format(game.createdAt).lower(),
			"teams": []
		}

		teams = model.Model().select(teamModel.Team).filter_by(gameId = game.id)

		for team in teams:
			teamData = {
				"id": team.id,
				"score": 0,
				"players": []
			}

			players = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(teamId = team.id)

			for player in players:
				user = model.Model().selectById(playerModel.Player, player.playerId)
				teamData["players"].append(user.name)

			scores = model.Model().select(scoreModel.Score).filter_by(gameId = game.id, teamId = team.id)

			for score in scores:
				if score.twenty:
					teamData["score"] += 20
				elif score.nineteen:
					teamData["score"] += 19
				elif score.eighteen:
					teamData["score"] += 18
				elif score.seventeen:
					teamData["score"] += 17
				elif score.sixteen:
					teamData["score"] += 16
				elif score.fifteen:
					teamData["score"] += 15
				elif score.bullseye:
					teamData["score"] += 25

			gameData["teams"].append(teamData)

		data.append(gameData)

		gameData["teams"].sort(key = operator.itemgetter("score"), reverse = True)

	return render_template("games/index.html", games = data)

@mod.route("/<int:id>/", methods = ["GET"])
def games_board(id):
	game = model.Model().selectById(gameModel.Game, id)
	teams = model.Model().select(teamModel.Team).filter_by(gameId = game.id)

	data = {
		"id": int(game.id),
		"teams": []
	}

	for team in teams:

		newTeam = {
			"id": team.id,
			"players": [],
			"scores": {
				20: 0,
				19: 0,
				18: 0,
				17: 0,
				16: 0,
				15: 0,
				25: 0
			}
		}

		players = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(teamId = team.id)

		for player in players:

			user = model.Model().selectById(playerModel.Player, player.playerId)

			newTeam["players"].append({
				"id": user.id,
				"name": user.name
			})

		scores = model.Model().select(scoreModel.Score).filter_by(gameId = game.id, teamId = team.id)

		for score in scores:
			if score.twenty:
				newTeam["scores"][20] += 1
			elif score.nineteen:
				newTeam["scores"][19] += 1
			elif score.eighteen:
				newTeam["scores"][18] += 1
			elif score.seventeen:
				newTeam["scores"][17] += 1
			elif score.sixteen:
				newTeam["scores"][16] += 1
			elif score.fifteen:
				newTeam["scores"][15] += 1
			elif score.bullseye:
				newTeam["scores"][25] += 1

		data["teams"].append(newTeam)

	return render_template("games/board.html", game = data)

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

	return Response(json.dumps({ "id": int(newScore.id) }), status = 200, mimetype = "application/json")