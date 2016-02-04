from darts import app
from flask import Response, render_template, redirect, request
from darts.entities import player as playerModel
from darts import model

@app.route("/brackets/", methods = ["GET"])
def brackets_index():
	return render_template("brackets/index.html")

@app.route("/brackets/new/", methods = ["GET"])
def brackets_new():
	players = model.Model().select(playerModel.Player).order_by("name")
	return render_template("brackets/new.html", players = players)

@app.route("/brackets/<int:id>/", methods = ["GET"])
def brackets_show(id):

	round1 = [1,21,10,24,3,22,6,4,13,12,5,18,11,14,2,23]
	round1Players = []
	for id in round1:
		round1Players.append(model.Model().selectById(playerModel.Player, id))

	round2 = [1,21,3,22,13,12,2,23]
	round2Players = []
	for id in round2:
		round2Players.append(model.Model().selectById(playerModel.Player, id))

	round3 = [0,0,0,0]
	round3Players = []
	for id in round3:
		round3Players.append(model.Model().selectById(playerModel.Player, id))

	round4 = [0,0]
	round4Players = []
	for id in round4:
		round4Players.append(model.Model().selectById(playerModel.Player, id))

	return render_template("brackets/show.html", round1Players = round1Players, round2Players = round2Players, round3Players = round3Players, round4Players = round4Players)
