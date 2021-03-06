from darts import app
from flask import Response, render_template, redirect, request
from darts.entities import match as matchModel
from darts.entities import player as playerModel
from darts.entities import team as teamModel
from darts.entities import team_player as teamPlayerModel
from darts.entities import mark as markModel
from darts.entities import result as resultModel
from darts.entities import mode as modeModel
from darts import model
from datetime import datetime
from sqlalchemy import desc
import operator, json, math

@app.route("/matches/", methods = ["GET"], defaults = { "page": 1 })
@app.route("/matches/<int:page>/", methods = ["GET"])
def matches_index(page):

	paging = {
		"total": 0,
		"page": page,
		"limit": 20,
		"pages": 0
	}

	data = []

	matches = model.Model().select(matchModel.Match).filter_by(ready = True, modeId = 1).order_by(desc("createdAt"))
	paging["total"] = matches.count()
	matches = matches.limit(paging["limit"]).offset((page - 1) * paging["limit"]).all()

	players = model.Model().select(playerModel.Player)
	playerDict = {}
	for player in players:
		playerDict[player.id] = player

	results = model.Model().select(resultModel.Result)
	resultDict = {}
	for result in results:
		if not resultDict.has_key(result.matchId):
			resultDict[result.matchId] = {}
		if not resultDict[result.matchId].has_key(result.teamId):
			resultDict[result.matchId][result.teamId] = []
		resultDict[result.matchId][result.teamId].append(result)

	for match in matches:

		matchData = {
			"id": match.id,
			"date": "{:%b %d, %Y} ".format(match.createdAt),
			"time": "{:%I:%M %p}".format(match.createdAt).lower(),
			"teams": []
		}

		teams = model.Model().select(teamModel.Team).filter_by(matchId = match.id)

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

			matchData["teams"].append(teamData)

		data.append(matchData)

		matchData["teams"].sort(key = operator.itemgetter("mark"), reverse = True)

	paging["pages"] = int(math.ceil(paging["total"] / float(paging["limit"])))

	return render_template("matches/index.html", matches = data, results = resultDict, paging = paging)

@app.route("/matches/new/", methods = ["GET"])
def matches_new():
	modes = model.Model().select(modeModel.Mode).filter_by(enabled = True)
	return render_template("matches/new.html", modes = modes)

@app.route("/matches/", methods = ["POST"])
def matches_create():
	newMatch = matchModel.Match(request.form["modes"], None, None, 1, 1, False, 0, datetime.now())
	model.Model().create(newMatch)

	mode = model.Model().selectById(modeModel.Mode, newMatch.modeId)
	return redirect("/matches/%d/modes/%s/" % (newMatch.id, mode.alias))
