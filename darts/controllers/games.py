from darts import app
from flask import Response, render_template, redirect, request
from darts.entities import game as gameModel
from darts.entities import player as playerModel
from darts.entities import team as teamModel
from darts.entities import team_player as teamPlayerModel
from darts.entities import mark as markModel
from darts.entities import result as resultModel
from darts.entities import mode as modeModel
from darts import model
from datetime import datetime
from sqlalchemy import desc
import operator
import json

@app.route("/games/", methods = ["GET"])
def games_index():

	data = []

	games = model.Model().select(gameModel.Game).filter_by(ready = True, modeId = 1).order_by(desc("createdAt"))

	players = model.Model().select(playerModel.Player)
	playerDict = {}
	for player in players:
		playerDict[player.id] = player

	results = model.Model().select(resultModel.Result)
	resultDict = {}
	for result in results:
		if not resultDict.has_key(result.gameId):
			resultDict[result.gameId] = {}
		if not resultDict[result.gameId].has_key(result.teamId):
			resultDict[result.gameId][result.teamId] = []
		resultDict[result.gameId][result.teamId].append(result)

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
				"points": 0,
				"win": team.win,
				"loss": team.loss
			}

			players = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(teamId = team.id)

			for player in players:
				teamData["players"].append(playerDict[player.playerId].name)

			gameData["teams"].append(teamData)

		data.append(gameData)

		gameData["teams"].sort(key = operator.itemgetter("mark"), reverse = True)

	return render_template("games/index.html", games = data, results = resultDict)

@app.route("/games/new/", methods = ["GET"])
def games_new():
	modes = model.Model().select(modeModel.Mode).filter_by(enabled = True)
	return render_template("games/new.html", modes = modes)

@app.route("/games/", methods = ["POST"])
def games_create():
	newGame = gameModel.Game(request.form["modes"], None, 1, 1, False, 0, datetime.now())
	model.Model().create(newGame)

	mode = model.Model().selectById(modeModel.Mode, newGame.modeId)
	return redirect("/games/%d/modes/%s/" % (newGame.id, mode.alias))
