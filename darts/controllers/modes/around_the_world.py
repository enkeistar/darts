from darts import app, model
from darts.entities import match as matchModel
from darts.entities import mode as modeModel
from darts.entities import mark as markModel
from darts.entities import player as playerModel
from darts.entities import team_player as teamPlayerModel
from darts.entities import team as teamModel
from flask import Response, render_template, redirect, request
from datetime import datetime
from sqlalchemy import text
import json

@app.route("/matches/<int:id>/modes/around-the-world/")
def around_the_world_index(id):
	return redirect("/matches/%d/modes/around-the-world/num-players/" % id)

@app.route("/matches/<int:id>/modes/around-the-world/num-players/")
def around_the_world_num_players(id):
	match = model.Model().selectById(matchModel.Match, id)
	mode = model.Model().selectById(modeModel.Mode, match.modeId)
	return render_template("matches/modes/x01/num-players.html", match = match, mode = mode)

@app.route("/matches/<int:id>/modes/around-the-world/num-players/", methods = ["POST"])
def around_the_world_num_players_update(id):
	match = model.Model().selectById(matchModel.Match, id)
	model.Model().update(matchModel.Match, match.id, { "players": request.form["players"] })

	for i in range(0, int(request.form["players"])):
		newTeam = teamModel.Team(match.id)
		model.Model().create(newTeam)

	return redirect("/matches/%d/modes/around-the-world/players/" % id)

@app.route("/matches/<int:id>/modes/around-the-world/players/")
def around_the_world_players(id):
	match = model.Model().selectById(matchModel.Match, id)
	mode = model.Model().selectById(modeModel.Mode, match.modeId)
	teamPlayers = getTeamPlayersByMatchId(match.id)
	teams = model.Model().select(teamModel.Team).filter_by(matchId = match.id)
	players = model.Model().select(playerModel.Player).order_by(playerModel.Player.name)
	return render_template("matches/modes/x01/players.html", match = match, mode = mode, teams = teams, players = players, teamPlayers = teamPlayers)

@app.route("/matches/<int:id>/modes/around-the-world/players/redo/", methods = ["POST"])
def around_the_world_players_redo(id):
	teamPlayers = getTeamPlayersByMatchId(id)

	for teamPlayer in teamPlayers:
		model.Model().delete(teamPlayerModel.TeamPlayer, teamPlayer.id)

	return redirect("/matches/%d/modes/around-the-world/players/" % id)

@app.route("/matches/<int:id>/modes/around-the-world/play/", methods = ["POST"])
def around_the_world_play_create(id):
	team = model.Model().select(teamModel.Team).filter_by(matchId = id).first()
	teamPlayer = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(teamId = team.id).first()
	match = model.Model().selectById(matchModel.Match, id)
	model.Model().update(matchModel.Match, match.id, { "ready": True, "turn": teamPlayer.playerId })
	return redirect("/matches/%d/modes/around-the-world/play/" % id)

@app.route("/matches/<int:id>/modes/around-the-world/play/", methods = ["GET"])
def around_the_world_play(id):
	data = {}
	data["match"] = model.Model().selectById(matchModel.Match, id)
	data["teamPlayers"] = getTeamPlayersByMatchId(id)
	data["teams"] = model.Model().select(teamModel.Team).filter_by(matchId = id)
	data["players"] = []

	for team in data["teams"]:
		players = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(teamId = team.id)
		for player in players:
			user = model.Model().selectById(playerModel.Player, player.playerId)
			data["players"].append({
				"id": user.id,
				"name": user.name,
				"teamId": team.id,
				"points": getPoints(id, user.id)
			})

	return render_template("matches/modes/around-the-world/board.html", data = data)

def getTeamPlayersByMatchId(matchId):
	teams = model.Model().select(teamModel.Team).filter_by(matchId = matchId)

	teamIds = []
	for team in teams:
		teamIds.append(team.id)

	teamPlayers = model.Model().select(teamPlayerModel.TeamPlayer).filter(teamPlayerModel.TeamPlayer.teamId.in_(teamIds)).order_by("id")

	return teamPlayers


@app.route("/matches/<int:matchId>/modes/around-the-world/teams/<int:teamId>/players/<int:playerId>/marks/<int:mark>/", methods = ["POST"])
def around_the_world_score(matchId, teamId, playerId, mark):

	newMark = markModel.Mark()
	newMark.matchId = matchId
	newMark.teamId = teamId
	newMark.playerId = playerId
	newMark.value = int(mark)
	newMark.createdAt = datetime.now()
	model.Model().create(newMark)

	return Response(json.dumps({ "id": int(newMark.id), "playerId": playerId, "mark": mark + 1 }), status = 200, mimetype = "application/json")

@app.route("/matches/<int:matchId>/modes/around-the-world/undo/", methods = ["POST"])
def around_the_world_undo(matchId):
	marks = model.Model().select(markModel.Mark).filter_by(matchId = matchId).order_by(markModel.Mark.id.desc())
	if marks.count() == 0:
		return ""

	mark = marks.first()
	model.Model().delete(markModel.Mark, mark.id)

	return Response(json.dumps({ "id": int(mark.id), "playerId": mark.playerId, "mark": mark.value }), status = 200, mimetype = "application/json")

def getPoints(matchId, playerId):
	query = "\
		SELECT MAX(Value) as points\
		FROM marks\
		WHERE matchId = :matchId\
			AND playerId = :playerId\
	"
	session = model.Model().getSession()
	connection = session.connection()
	data = connection.execute(text(query), matchId = matchId, playerId = playerId).first()
	if data.points == None:
		return 1
	else:
		return data.points + 1
