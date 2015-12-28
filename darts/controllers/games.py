from darts import app
from flask import Blueprint, Response, render_template, redirect, request
from darts.entities import game as gameModel, player as playerModel, team as teamModel, team_player as teamPlayerModel, mark as markModel
from darts import model
from datetime import datetime
from sqlalchemy import desc
import operator
import json

mod = Blueprint("games", __name__, url_prefix = "/games")

@mod.route("/", methods = ["GET"])
def games_index():

	data = []

	games = model.Model().select(gameModel.Game).filter_by(ready = True).order_by(desc("createdAt"))

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
				"mark": 0,
				"players": [],
				"points": 0
			}

			players = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(teamId = team.id)

			for player in players:
				user = model.Model().selectById(playerModel.Player, player.playerId)
				teamData["players"].append(user.name)

			marks = model.Model().select(markModel.Mark).filter_by(gameId = game.id, teamId = team.id)

			for mark in marks:
				if mark.twenty:
					teamData["mark"] += 20
				elif mark.nineteen:
					teamData["mark"] += 19
				elif mark.eighteen:
					teamData["mark"] += 18
				elif mark.seventeen:
					teamData["mark"] += 17
				elif mark.sixteen:
					teamData["mark"] += 16
				elif mark.fifteen:
					teamData["mark"] += 15
				elif mark.bullseye:
					teamData["mark"] += 25

			gameData["teams"].append(teamData)

		data.append(gameData)

		gameData["teams"].sort(key = operator.itemgetter("mark"), reverse = True)

	return render_template("games/index.html", games = data)

@mod.route("/<int:id>/", methods = ["GET"])
def games_board(id):
	game = model.Model().selectById(gameModel.Game, id)
	teams = model.Model().select(teamModel.Team).filter_by(gameId = game.id)

	data = {
		"id": int(game.id),
		"game": game.game,
		"round": game.round,
		"players": game.players,
		"teams": []
	}

	for team in teams:

		teamData = {
			"id": team.id,
			"players": [],
			"marks": [{
				20: 0,
				19: 0,
				18: 0,
				17: 0,
				16: 0,
				15: 0,
				25: 0,
				"points": 0
			}, {
				20: 0,
				19: 0,
				18: 0,
				17: 0,
				16: 0,
				15: 0,
				25: 0,
				"points": 0
			}, {
				20: 0,
				19: 0,
				18: 0,
				17: 0,
				16: 0,
				15: 0,
				25: 0,
				"points": 0
			}]
		}

		players = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(teamId = team.id)

		for player in players:

			user = model.Model().selectById(playerModel.Player, player.playerId)

			teamData["players"].append({
				"id": user.id,
				"name": user.name
			})

		for i in range(0,3):

			scored = {
				"twenty": 0,
				"nineteen": 0,
				"eighteen": 0,
				"seventeen": 0,
				"sixteen": 0,
				"fifteen": 0,
				"bullseye": 0
			}
			pointsScored = 0

			marks = model.Model().select(markModel.Mark).filter_by(gameId = game.id, teamId = team.id, game = i + 1)

			for mark in marks:
				if mark.twenty:
					teamData["marks"][i][20] += 1
					scored["twenty"] += 1
					if scored["twenty"] > 3:
						pointsScored += 20
				elif mark.nineteen:
					teamData["marks"][i][19] += 1
					scored["nineteen"] += 1
					if scored["nineteen"] > 3:
						pointsScored += 19
				elif mark.eighteen:
					teamData["marks"][i][18] += 1
					scored["eighteen"] += 1
					if scored["eighteen"] > 3:
						pointsScored += 18
				elif mark.seventeen:
					teamData["marks"][i][17] += 1
					scored["seventeen"] += 1
					if scored["seventeen"] > 3:
						pointsScored += 17
				elif mark.sixteen:
					teamData["marks"][i][16] += 1
					scored["sixteen"] += 1
					if scored["sixteen"] > 3:
						pointsScored += 16
				elif mark.fifteen:
					teamData["marks"][i][15] += 1
					scored["fifteen"] += 1
					if scored["fifteen"] > 3:
						pointsScored += 15
				elif mark.bullseye:
					teamData["marks"][i][25] += 1
					scored["bullseye"] += 1
					if scored["bullseye"] > 3:
						pointsScored += 25

			teamData["marks"][i]["points"] = pointsScored

		data["teams"].append(teamData)

	return render_template("games/board.html", game = data)

@mod.route("/new/", methods = ["GET"])
def games_new():
	return render_template("games/new.html")

@mod.route("/", methods = ["POST"])
def games_create():
	newGame = gameModel.Game(request.form["players"], 1, 1, False, datetime.now())
	model.Model().create(newGame)

	teams = 2

	if newGame.players == 3:
		teams = 3

	for i in range(0, teams):
		newTeam = teamModel.Team(newGame.id)
		model.Model().create(newTeam)

	return redirect("/games/%d/players/" % newGame.id)

@mod.route("/<int:id>/play/", methods = ["POST"])
def games_play(id):
	game = model.Model().selectById(gameModel.Game, id)
	model.Model().update(gameModel.Game, game.id, { "ready": True })
	return redirect("/games/%d/" % id)

@mod.route("/<int:id>/players/", methods = ["GET"])
def games_players(id):
	game = model.Model().selectById(gameModel.Game, id)
	teams = model.Model().select(teamModel.Team).filter_by(gameId = game.id)
	players = model.Model().select(playerModel.Player)

	teamIds = []
	for team in teams:
		teamIds.append(team.id)

	teamPlayers = model.Model().select(teamPlayerModel.TeamPlayer).filter(teamPlayerModel.TeamPlayer.teamId.in_(teamIds))

	return render_template("games/players.html", game = game, teams = teams, players = players, teamPlayers = teamPlayers)

@mod.route("/<int:id>/players/", methods = ["POST"])
def games_players_create(id):
	teamPlayer = teamPlayerModel.TeamPlayer(request.form["teamId"], request.form["playerId"])
	model.Model().create(teamPlayer)
	return Response(json.dumps({ "id": int(teamPlayer.id) }), status = 200, mimetype = "application/json")

@mod.route("/<int:id>/", methods = ["POST"])
def games_start(id):
	game = model.Model().selectById(gameModel.Game, id)

	team1Player1 = teamPlayerModel.TeamPlayer(newTeam1.id, request.form["team-1-player-1-id"])
	model.Model().create(team1Player1)

	team2Player1 = teamPlayerModel.TeamPlayer(newTeam2.id, request.form["team-2-player-1-id"])
	model.Model().create(team2Player1)

	if game.players == 4:
		team1Player2 = teamPlayerModel.TeamPlayer(newTeam1.id, request.form["team-1-player-2-id"])
		model.Model().create(team1Player2)

		team2Player2 = teamPlayerModel.TeamPlayer(newTeam2.id, request.form["team-2-player-2-id"])
		model.Model().create(team2Player2)

	return redirect("/games/%d/" % id)

@mod.route("/<int:id>/players/redo/", methods = ["POST"])
def games_players_redo(id):
	teams = model.Model().select(teamModel.Team).filter_by(gameId = id)

	teamIds = []
	for team in teams:
		teamIds.append(team.id)

	teamPlayers = model.Model().select(teamPlayerModel.TeamPlayer).filter(teamPlayerModel.TeamPlayer.teamId.in_(teamIds))

	for teamPlayer in teamPlayers:
		model.Model().delete(teamPlayerModel.TeamPlayer, teamPlayer.id)

	return redirect("/games/%d/players/" % id)

@mod.route("/<int:id>/next/", methods = ["POST"])
def games_next(id):
	game = model.Model().selectById(gameModel.Game, id)

	if game.game < 3:
		model.Model().update(gameModel.Game, game.id, { "game": game.game + 1, "round": 1 })
		return redirect("/games/%d/" % game.id)
	else:
		return redirect("/")

@mod.route("/<int:gameId>/teams/<int:teamId>/players/<int:playerId>/games/<int:game>/rounds/<int:round>/marks/<int:mark>/", methods = ["POST"])
def games_score(gameId, teamId, playerId, game, round, mark):

	model.Model().update(gameModel.Game, gameId, { "round": round })

	newMark = markModel.Mark()
	newMark.gameId = gameId
	newMark.teamId = teamId
	newMark.playerId = playerId
	newMark.game = game
	newMark.round = round
	newMark.createdAt = datetime.now()

	points = int(mark)

	if points == 20:
		newMark.twenty = 1
	elif points == 19:
		newMark.nineteen = 1
	elif points == 18:
		newMark.eighteen = 1
	elif points == 17:
		newMark.seventeen = 1
	elif points == 16:
		newMark.sixteen = 1
	elif points == 15:
		newMark.fifteen = 1
	elif points == 25:
		newMark.bullseye = 1

	model.Model().create(newMark)

	return Response(json.dumps({ "id": int(newMark.id) }), status = 200, mimetype = "application/json")

@mod.route("/<int:gameId>/teams/<int:teamId>/players/<int:playerId>/games/<int:game>/undo/", methods = ["POST"])
def games_undo(gameId, teamId, playerId, game):

	id = 0

	marks = model.Model().select(markModel.Mark).filter_by(gameId = gameId, teamId = teamId, playerId = playerId, game = game)

	if marks.count() > 0:
		id = marks[marks.count() - 1].id
		model.Model().delete(markModel.Mark, id)

	return Response(json.dumps({ "id": id }), status = 200, mimetype = "application/json")

