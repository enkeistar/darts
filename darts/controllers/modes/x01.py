from darts import app, model
from darts.entities import match as matchModel
from darts.entities import team as teamModel
from darts.entities import mode as modeModel
from darts.entities import mark as markModel
from darts.entities import player as playerModel
from darts.entities import team_player as teamPlayerModel
from flask import render_template, request, redirect, Response
from datetime import datetime
import json

@app.route("/games/<int:id>/modes/x01/", methods = ["GET"])
def x01_index(id):
	game = model.Model().selectById(matchModel.Match, id)
	return render_template("games/modes/x01/num-players.html", game = game)

@app.route("/games/<int:id>/modes/x01/num-players/", methods = ["POST"])
def x01_create_num_players(id):
	game = model.Model().selectById(matchModel.Match, id)
	model.Model().update(matchModel.Match, game.id, { "players": request.form["players"] })

	for i in range(0, int(request.form["players"])):
		newTeam = teamModel.Team(game.id)
		model.Model().create(newTeam)

	return redirect("/games/%d/modes/x01/players/" % game.id)

@app.route("/games/<int:id>/modes/x01/players/", methods = ["GET"])
def x01_players(id):
	game = model.Model().selectById(matchModel.Match, id)
	mode = model.Model().selectById(modeModel.Mode, game.modeId)
	teamPlayers = getTeamPlayersByGameId(game.id)
	teams = model.Model().select(teamModel.Team).filter_by(gameId = game.id)
	players = model.Model().select(playerModel.Player).order_by(playerModel.Player.name)
	return render_template("games/modes/x01/players.html", game = game, teams = teams, players = players, teamPlayers = teamPlayers)

@app.route("/games/<int:id>/modes/x01/players/", methods = ["POST"])
def x01_players_create(id):
	teamPlayer = teamPlayerModel.TeamPlayer(request.form["teamId"], request.form["playerId"])
	model.Model().create(teamPlayer)
	return Response(json.dumps({ "id": int(teamPlayer.id) }), status = 200, mimetype = "application/json")

@app.route("/games/<int:id>/modes/x01/players/redo/", methods = ["POST"])
def x01_players_redo(id):
	teamPlayers = getTeamPlayersByGameId(id)

	for teamPlayer in teamPlayers:
		model.Model().delete(teamPlayerModel.TeamPlayer, teamPlayer.id)

	return redirect("/games/%d/modes/x01/players/" % id)

@app.route("/games/<int:id>/modes/x01/play/", methods = ["POST"])
def x01_play_create(id):
	team = model.Model().select(teamModel.Team).filter_by(gameId = id).first()
	teamPlayer = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(teamId = team.id).first()
	game = model.Model().selectById(matchModel.Match, id)
	model.Model().update(matchModel.Match, game.id, { "ready": True, "turn": teamPlayer.playerId })
	return redirect("/games/%d/modes/x01/play/" % id)

@app.route("/games/<int:id>/modes/x01/play/", methods = ["GET"])
def x01_play(id):
	game = model.Model().selectById(matchModel.Match, id)
	mode = model.Model().selectById(modeModel.Mode, game.modeId)
	teamPlayers = getTeamPlayersByGameId(game.id)
	teams = model.Model().select(teamModel.Team).filter_by(gameId = game.id)

	data = {
		"id": int(game.id),
		"game": game.game,
		"round": game.round,
		"players": game.players,
		"num-players": 0,
		"turn": game.turn,
		"complete": game.complete,
		"players": [],
		"mode": mode
	}

	for team in teams:
		players = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(teamId = team.id)

		for player in players:

			user = model.Model().selectById(playerModel.Player, player.playerId)
			teamPlayer = teamPlayers.filter_by(playerId = user.id).one()
			marks = model.Model().select(markModel.Mark).filter_by(gameId = game.id, playerId = player.playerId)
			playerPoints = int(mode.mode)

			for mark in marks:
				playerPoints -= mark.value

			data["players"].append({
				"id": user.id,
				"name": user.name,
				"teamId": teamPlayer.teamId,
				"points": playerPoints
			})

	data["num-players"] = len(data["players"])

	return render_template("games/modes/x01/board.html", data = data)

@app.route("/games/<int:gameId>/modes/x01/teams/<int:teamId>/players/<int:playerId>/games/<int:game>/rounds/<int:round>/marks/<int:mark>/", methods = ["POST"])
def x01_score(gameId, teamId, playerId, game, round, mark):

	model.Model().update(matchModel.Match, gameId, { "round": round })

	newMark = markModel.Mark()
	newMark.gameId = gameId
	newMark.teamId = teamId
	newMark.playerId = playerId
	newMark.game = game
	newMark.round = round
	newMark.value = int(mark)
	newMark.createdAt = datetime.now()

	model.Model().create(newMark)

	return Response(json.dumps({ "id": int(newMark.id) }), status = 200, mimetype = "application/json")

@app.route("/games/<int:gameId>/modes/x01/players/<int:playerId>/turn/", methods = ["POST"])
def x01_turn(gameId, playerId):
	model.Model().update(matchModel.Match, gameId, { "turn": playerId })
	return Response(json.dumps({ "id": gameId }), status = 200, mimetype = "application/json")

@app.route("/games/<int:gameId>/modes/x01/undo/", methods = ["POST"])
def x01_undo(gameId):
	marks = model.Model().select(markModel.Mark).filter_by(gameId = gameId).order_by(markModel.Mark.id.desc())

	if marks.count() > 0:
		mark = marks.first()
		model.Model().update(matchModel.Match, gameId, { "turn": mark.playerId })
		model.Model().delete(markModel.Mark, mark.id)
		return Response(json.dumps({  "gameId": gameId, "playerId": mark.playerId, "value": mark.value, "valid": True }), status = 200, mimetype = "application/json")

	return Response(json.dumps({ "id": gameId, "valid": False }), status = 200, mimetype = "application/json")

def getTeamPlayersByGameId(gameId):
	teams = model.Model().select(teamModel.Team).filter_by(gameId = gameId)

	teamIds = []
	for team in teams:
		teamIds.append(team.id)

	teamPlayers = model.Model().select(teamPlayerModel.TeamPlayer).filter(teamPlayerModel.TeamPlayer.teamId.in_(teamIds)).order_by("id")

	return teamPlayers
