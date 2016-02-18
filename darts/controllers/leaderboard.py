from darts import app
from flask import Response, render_template, redirect, request
from darts.entities import game as gameModel
from darts.entities import player as playerModel
from darts.entities import team as teamModel
from darts.entities import team_player as teamPlayerModel
from darts.entities import mark as markModel
from darts.entities import result as resultModel
from darts import model
from sqlalchemy import text
from datetime import datetime, timedelta

@app.route("/leaderboard/", methods = ["GET"])
def leaderboard_index():

	start = request.args.get("start")
	end = request.args.get("end")

	useStart = start is not None and len(start) > 0
	useEnd = end is not None and len(end) > 0

	if useEnd:
		date = datetime.strptime(end , "%Y-%m-%d")
		end = date + timedelta(days = 1)

	query = "\
		SELECT\
			p.id,\
			p.name,\
			(\
				SELECT COUNT(*)\
				FROM teams_players tp\
				LEFT JOIN teams t ON tp.teamId = t.id\
				LEFT JOIN games g on t.gameId = g.id\
				WHERE tp.playerId = p.id AND g.modeId = 1 AND g.complete = 1\
	"

	if useStart:
		query += "\
			AND g.createdAt >= :start\
		"
	if useEnd:
		query += "\
			AND g.createdAt < :end\
		"

	query += "\
			) AS games,\
			(\
				SELECT COUNT(*)\
				FROM marks m\
				LEFT JOIN games g on m.gameId = g.id\
				WHERE 1 = 1\
					AND m.playerId = p.id\
					AND m.value != 0\
					AND g.modeId = 1\
					AND g.complete = 1\
	"

	if useStart:
		query += "\
			AND g.createdAt >= :start\
		"
	if useEnd:
		query += "\
			AND g.createdAt < :end\
		"

	query += "\
			) AS marks,\
			(\
				SELECT COUNT(playerId) \
				FROM (\
					SELECT r.playerId, r.gameId, r.teamId, r.game, r.round\
					FROM marks r\
					LEFT JOIN games g on r.gameId = g.id\
					WHERE g.modeId = 1 AND g.complete = 1\
	"

	if useStart:
		query += "\
			AND g.createdAt >= :start\
		"
	if useEnd:
		query += "\
			AND g.createdAt < :end\
		"

	query += "\
					GROUP BY r.playerId, r.gameId, r.teamId, r.round, r.game\
				) AS rounds\
				WHERE playerId = p.id\
			) AS rounds,\
			(\
				SELECT COUNT(*)\
				FROM players p2\
				LEFT JOIN teams_players tp2 on tp2.playerId = p2.id\
				LEFT JOIN teams t2 on tp2.teamId = t2.id\
				LEFT JOIN games g on t2.gameId = g.id\
				WHERE g.modeId = 1 AND t2.win = 1 AND p2.id = p.id\
	"

	if useStart:
		query += "\
			AND g.createdAt >= :start\
		"
	if useEnd:
		query += "\
			AND g.createdAt < :end\
		"

	query += "\
			) AS wins\
			,\
			(\
				SELECT COUNT(*)\
				FROM players p2\
				LEFT JOIN teams_players tp2 on tp2.playerId = p2.id\
				LEFT JOIN teams t2 on tp2.teamId = t2.id\
				LEFT JOIN games g on t2.gameId = g.id\
				WHERE g.modeId = 1 AND t2.loss = 1 AND p2.id = p.id\
	"

	if useStart:
		query += "\
			AND g.createdAt >= :start\
		"
	if useEnd:
		query += "\
			AND g.createdAt < :end\
		"

	query += "\
			) AS losses\
		FROM players p\
		ORDER BY name;\
	"

	session = model.Model().getSession()
	connection = session.connection()
	data = connection.execute(text(query), start = start, end = end)

	points = getPlayerPoints(start, useStart, end, useEnd)
	times = getTimePlayed(start, useStart, end, useEnd)

	if request.is_xhr:
		return render_template("leaderboard/_table.html", data = data, points = points, times = times)
	else:
		return render_template("leaderboard/index.html", data = data, points = points, times = times)


def getPlayerPoints(start, useStart, end, useEnd):

	data = {}

	query = "\
		SELECT m.*\
		FROM marks m\
		LEFT JOIN games g ON m.gameId = g.id\
		WHERE g.modeId = 1 AND g.complete = 1\
	"

	if useStart:
		query += "\
			AND g.createdAt >= :start\
		"
	if useEnd:
		query += "\
			AND g.createdAt < :end\
		"

	session = model.Model().getSession()
	connection = session.connection()
	marks = connection.execute(text(query), start = start, end = end)

	points = {}
	players = model.Model().select(playerModel.Player)

	for player in players:
		points[player.id] = 0

	for mark in marks:

		if not data.has_key(mark.gameId):
			data[mark.gameId] = {}

		if not data[mark.gameId].has_key(mark.teamId):
			data[mark.gameId][mark.teamId] = {}

		if not data[mark.gameId][mark.teamId].has_key(mark.game):
			data[mark.gameId][mark.teamId][mark.game] = {}

		if not data[mark.gameId][mark.teamId][mark.game].has_key(mark.value):
			data[mark.gameId][mark.teamId][mark.game][mark.value] = 0

		data[mark.gameId][mark.teamId][mark.game][mark.value] += 1

		if data[mark.gameId][mark.teamId][mark.game][mark.value] > 3:
			points[mark.playerId] += mark.value

	return points

def getTimePlayed(start, useStart, end, useEnd):

	times = {}
	players = model.Model().select(playerModel.Player)

	for player in players:
		times[player.id] = {
			"seconds": 0,
			"time": ""
		}

	query = "\
		SELECT DISTINCT p.id as playerId, g.id as gameId, UNIX_TIMESTAMP(g.createdAt) as gameTime, (\
			SELECT UNIX_TIMESTAMP(r.createdAt)\
			FROM results r\
			WHERE r.gameId = g.id AND r.teamId = t.id\
			ORDER BY r.id DESC\
			LIMIT 1\
		) as resultTime\
		FROM players p\
		LEFT JOIN teams_players tp ON p.id = tp.playerId\
		LEFT JOIN teams t ON tp.teamId = t.id\
		LEFT JOIN games g ON t.gameId = g.id\
		WHERE g.complete = 1 AND g.modeId = 1\
	"

	if useStart:
		query += "\
			AND g.createdAt >= :start\
		"
	if useEnd:
		query += "\
			AND g.createdAt < :end\
		"

	session = model.Model().getSession()
	connection = session.connection()
	rows = connection.execute(text(query), start = start, end = end)

	for row in rows:
		times[row.playerId]["seconds"] += row.resultTime - row.gameTime

	for playerId in times:
		times[playerId]["time"] = formatTime(times[playerId]["seconds"])

	return times

def formatTime(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	return "%02d:%02d:%02d" % (h, m, s)
