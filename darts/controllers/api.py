from darts import app
from flask import Response, render_template, redirect, request
from darts.entities import game as gameModel, player as playerModel, team as teamModel, team_player as teamPlayerModel, mark as markModel, result as resultModel
from darts import model
import json

@app.route("/api/", methods = ["GET"])
def api_index():
	return render_template("api/index.html")

@app.route("/api/players/", methods = ["GET"])
def api_players():
	players = model.Model().select(playerModel.Player)

	data = []

	for player in players:
		data.append({
			"id": player.id,
			"name": player.name,
			"createdAt": str(player.createdAt)
		})

	return json_response(data)

@app.route("/api/games/", methods = ["GET"])
def api_games():
	games = model.Model().select(gameModel.Game)

	data = []

	for game in games:
		data.append({
			"id": game.id,
			"players": game.players,
			"game": game.game,
			"round": game.round,
			"ready": toBoolean(game.ready),
			"turn": game.turn,
			"complete": toBoolean(game.complete),
			"createdAt": str(game.createdAt)
		})

	return json_response(data)

@app.route("/api/marks/", methods = ["GET"])
def api_marks():
	marks = model.Model().select(markModel.Mark)

	data = []

	for mark in marks:
		data.append({
			"id": mark.id,
			"gameId": mark.gameId,
			"teamId": mark.teamId,
			"playerId": mark.playerId,
			"game": mark.game,
			"round": mark.round,
			"value": mark.value,
			"createdAt": str(mark.createdAt)
		})

	return json_response(data)

@app.route("/api/teams/", methods = ["GET"])
def api_teams():
	teams = model.Model().select(teamModel.Team)

	data = []

	for team in teams:
		data.append({
			"id": team.id,
			"gameId": team.gameId,
			"win": toBoolean(team.win),
			"loss": toBoolean(team.loss)
		})

	return json_response(data)

@app.route("/api/teams-players/", methods = ["GET"])
def api_teams_players():
	teamPlayers = model.Model().select(teamPlayerModel.TeamPlayer)

	data = []

	for teamPlayer in teamPlayers:
		data.append({
			"id": teamPlayer.id,
			"teamId": teamPlayer.teamId,
			"playerId": teamPlayer.playerId
		})

	return json_response(data)

def json_response(data):
	return Response(json.dumps(data), status = 200, mimetype = "application/json")

def toBoolean(value):
	if(value == 1):
		return True
	else:
		return False

