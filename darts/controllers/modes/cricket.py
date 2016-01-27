from darts import app, model
from darts.entities import game as gameModel
from darts.entities import player as playerModel
from darts.entities import team as teamModel
from darts.entities import team_player as teamPlayerModel
from darts.entities import mark as markModel
from darts.entities import result as resultModel
from darts.entities import mode as modeModel
from flask import Response, render_template, redirect, request
from datetime import datetime
import json

@app.route("/games/<int:id>/modes/cricket/")
def cricket_index(id):
	game = model.Model().selectById(gameModel.Game, id)
	return render_template("games/modes/cricket/num-players.html", game = game)

@app.route("/games/<int:id>/modes/cricket/num-players/", methods = ["POST"])
def cricket_create_num_players(id):
	game = model.Model().selectById(gameModel.Game, id)
	model.Model().update(gameModel.Game, game.id, { "players": request.form["players"] })

	for i in range(0, 2):
		newTeam = teamModel.Team(game.id)
		model.Model().create(newTeam)

	return redirect("/games/%d/modes/cricket/players/" % game.id)

@app.route("/games/<int:id>/modes/cricket/play/", methods = ["GET"])
def cricket_board(id):
	game = model.Model().selectById(gameModel.Game, id)
	mode = model.Model().selectById(modeModel.Mode, game.modeId)
	results = model.Model().select(resultModel.Result).filter_by(gameId = game.id)
	teams = model.Model().select(teamModel.Team).filter_by(gameId = game.id)

	data = {
		"id": int(game.id),
		"game": game.game,
		"round": game.round,
		"players": game.players,
		"turn": game.turn,
		"teams": [],
		"results": results,
		"complete": game.complete,
		"mode": mode
	}

	for team in teams:

		teamData = {
			"id": team.id,
			"players": [],
			"marks": {
				20: 0,
				19: 0,
				18: 0,
				17: 0,
				16: 0,
				15: 0,
				25: 0,
				0: 0,
				"points": 0
			},
			"results": []
		}

		for i in range(1, 4):
			results = model.Model().select(resultModel.Result).filter_by(gameId = game.id, teamId = team.id, game = i)
			resultSet = {
				"score": 0,
				"win": 0,
				"loss": 0
			}

			if results.count() > 0:
				result = results.first()
				resultSet["score"] = result.score
				resultSet["win"] = result.win
				resultSet["loss"] = result.loss

			teamData["results"].append(resultSet)

		players = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(teamId = team.id)

		for player in players:

			user = model.Model().selectById(playerModel.Player, player.playerId)

			teamData["players"].append({
				"id": user.id,
				"name": user.name
			})

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
		pointsScored = 0

		marks = model.Model().select(markModel.Mark).filter_by(gameId = game.id, teamId = team.id, game = game.game)

		for mark in marks:
			teamData["marks"][mark.value] += 1
			scored[mark.value] += 1
			if scored[mark.value] > 3:
				pointsScored += mark.value

		teamData["marks"]["points"] = pointsScored

		data["teams"].append(teamData)

	return render_template("games/modes/cricket/board.html", game = data)

@app.route("/games/<int:id>/modes/cricket/play/", methods = ["POST"])
def cricket_play(id):
	team = model.Model().select(teamModel.Team).filter_by(gameId = id).first()
	teamPlayer = model.Model().select(teamPlayerModel.TeamPlayer).filter_by(teamId = team.id).first()
	game = model.Model().selectById(gameModel.Game, id)
	model.Model().update(gameModel.Game, game.id, { "ready": True, "turn": teamPlayer.playerId })
	return redirect("/games/%d/modes/cricket/play/" % id)

@app.route("/games/<int:id>/modes/cricket/players/", methods = ["GET"])
def cricket_players(id):
	game = model.Model().selectById(gameModel.Game, id)
	mode = model.Model().selectById(modeModel.Mode, game.modeId)
	teamPlayers = getTeamPlayersByGameId(game.id)
	teams = model.Model().select(teamModel.Team).filter_by(gameId = game.id)
	players = model.Model().select(playerModel.Player).order_by(playerModel.Player.name)
	return render_template("games/modes/cricket/players.html", game = game, teams = teams, players = players, teamPlayers = teamPlayers)

@app.route("/games/<int:id>/modes/cricket/players/", methods = ["POST"])
def cricket_players_create(id):
	teamPlayer = teamPlayerModel.TeamPlayer(request.form["teamId"], request.form["playerId"])
	model.Model().create(teamPlayer)
	return Response(json.dumps({ "id": int(teamPlayer.id) }), status = 200, mimetype = "application/json")

@app.route("/games/<int:id>/modes/cricket/", methods = ["POST"])
def cricket_start(id):
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

	return redirect("/games/%d/modes/cricket/" % id)

@app.route("/games/<int:id>/modes/cricket/players/redo/", methods = ["POST"])
def cricket_players_redo(id):
	teamPlayers = getTeamPlayersByGameId(id)

	for teamPlayer in teamPlayers:
		model.Model().delete(teamPlayerModel.TeamPlayer, teamPlayer.id)

	return redirect("/games/%d/modes/cricket/players/" % id)

@app.route("/games/<int:id>/modes/cricket/next/", methods = ["POST"])
def cricket_next(id):
	game = model.Model().selectById(gameModel.Game, id)

	gameNum = game.game + 1

	if game.complete:
		return redirect("/")

	teamPlayers = getTeamPlayersByGameId(game.id)

	if game.players == 4:
		if gameNum == 2:
			turn = teamPlayers[2].playerId
		else:
			turn = teamPlayers[1].playerId
	else:
		if gameNum == 2:
			turn = teamPlayers[1].playerId
		else:
			turn = teamPlayers[0].playerId

	model.Model().update(gameModel.Game, game.id, { "game": gameNum, "round": 1, "turn": turn })

	return redirect("/games/%d/modes/cricket/play/" % game.id)

@app.route("/games/<int:gameId>/modes/cricket/teams/<int:teamId>/players/<int:playerId>/games/<int:game>/rounds/<int:round>/marks/<int:mark>/", methods = ["POST"])
def cricket_score(gameId, teamId, playerId, game, round, mark):

	model.Model().update(gameModel.Game, gameId, { "round": round })

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

@app.route("/games/<int:gameId>/modes/cricket/undo/", methods = ["POST"])
def cricket_undo(gameId):
	marks = model.Model().select(markModel.Mark).filter_by(gameId = gameId).order_by(markModel.Mark.id.desc())

	if marks.count() > 0:
		mark = marks.first()
		model.Model().update(gameModel.Game, gameId, { "turn": mark.playerId })
		model.Model().delete(markModel.Mark, mark.id)
		return Response(json.dumps({  "gameId": gameId, "teamId": mark.teamId, "playerId": mark.playerId, "value": mark.value, "valid": True }), status = 200, mimetype = "application/json")

	return Response(json.dumps({ "id": gameId, "valid": False }), status = 200, mimetype = "application/json")

@app.route("/games/<int:gameId>/modes/cricket/players/<int:playerId>/turn/", methods = ["POST"])
def cricket_turn(gameId, playerId):
	model.Model().update(gameModel.Game, gameId, { "turn": playerId })
	return Response(json.dumps({ "id": gameId }), status = 200, mimetype = "application/json")

@app.route("/games/<int:gameId>/modes/cricket/teams/<int:teamId>/game/<int:game>/score/<int:score>/win/", methods = ["POST"])
def cricket_win(gameId, teamId, game, score):
	return result(gameId, teamId, game, score, 1, 0)

@app.route("/games/<int:gameId>/modes/cricket/teams/<int:teamId>/game/<int:game>/score/<int:score>/loss/", methods = ["POST"])
def cricket_loss(gameId, teamId, game, score):
	return result(gameId, teamId, game, score, 0, 1)

@app.route("/games/<int:gameId>/modes/cricket/teams/<int:teamId>/win/", methods = ["POST"])
def cricket_gameWin(gameId, teamId):
	return gameResult(gameId, teamId, 1, 0)

@app.route("/games/<int:gameId>/modes/cricket/teams/<int:teamId>/loss/", methods = ["POST"])
def cricket_gameLoss(gameId, teamId):
	return gameResult(gameId, teamId, 0, 1)

def result(gameId, teamId, game, score, win, loss):
	newResult = resultModel.Result(gameId, teamId, game, score, win, loss, datetime.now())
	model.Model().create(newResult)
	return Response(json.dumps({ "id": gameId }), status = 200, mimetype = "application/json")

def gameResult(gameId, teamId, win, loss):
	model.Model().update(teamModel.Team, teamId, { "win": win, "loss": loss })
	if win == 1:
		model.Model().update(gameModel.Game, gameId, { "complete": 1 })
	return Response(json.dumps({ "id": teamId }), status = 200, mimetype = "application/json")

def getTeamPlayersByGameId(gameId):
	teams = model.Model().select(teamModel.Team).filter_by(gameId = gameId)

	teamIds = []
	for team in teams:
		teamIds.append(team.id)

	teamPlayers = model.Model().select(teamPlayerModel.TeamPlayer).filter(teamPlayerModel.TeamPlayer.teamId.in_(teamIds)).order_by("id")

	return teamPlayers

