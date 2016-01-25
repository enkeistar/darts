from darts import app
from flask import Blueprint, Response, render_template, redirect
from darts.entities import game as gameModel, player as playerModel, team as teamModel, team_player as teamPlayerModel, mark as markModel, result as resultModel
from darts import model

mod = Blueprint("leaderboard", __name__, url_prefix = "/leaderboard")

@mod.route("/", methods = ["GET"])
def leaderboard_index():

	session = model.Model().getSession()
	connection = session.connection()
	data = connection.execute("\
		SELECT\
			p.id,\
			p.name,\
			(\
				SELECT COUNT(*)\
				FROM teams_players tp\
				LEFT JOIN teams t ON tp.teamId = t.id\
				LEFT JOIN games g on t.gameId = g.id\
				WHERE tp.playerId = p.id AND g.complete = 1\
			) AS games,\
			(\
				SELECT COUNT(*)\
				FROM marks m\
				LEFT JOIN games g on m.gameId = g.id\
				WHERE m.playerId = p.id AND g.complete = 1\
			) AS marks,\
			(\
				SELECT COUNT(playerId) \
				FROM (\
					SELECT r.playerId, r.gameId, r.teamId, r.game, r.round\
					FROM marks r\
					LEFT JOIN games g on r.gameId = g.id\
					WHERE g.complete = 1\
					GROUP BY r.playerId, r.gameId, r.teamId, r.round, r.game\
				) AS rounds\
				WHERE playerId = p.id\
			) AS rounds,\
			(\
				SELECT COUNT(*)\
				FROM players p2\
				LEFT JOIN teams_players tp2 on tp2.playerId = p2.id\
				LEFT JOIN teams t2 on tp2.teamId = t2.id\
				WHERE t2.win = 1 AND p2.id = p.id\
			) AS wins\
			,\
			(\
				SELECT COUNT(*)\
				FROM players p2\
				LEFT JOIN teams_players tp2 on tp2.playerId = p2.id\
				LEFT JOIN teams t2 on tp2.teamId = t2.id\
				WHERE t2.loss = 1 AND p2.id = p.id\
			) AS losses\
		FROM players p\
		ORDER BY name;\
	")

	return render_template("leaderboard/index.html", data = data)
