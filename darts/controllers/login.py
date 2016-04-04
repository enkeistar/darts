from darts import app
from flask import request, render_template, redirect, session
from darts.entities import player as playerModel
from darts import model
import hashlib

@app.route("/login/")
def login_form():
	return render_template("login/form.html")

@app.route("/login/", methods = ["POST"])
def login_authenticate():

	player = model.Model().select(playerModel.Player).filter_by(username = request.form["username"])

	if player.count() != 1:
		return redirect("/login/")

	if hashlib.sha224(request.form["password"]).hexdigest() == player.first().password:
		session["authenticated"] = True
		session.save()
		return redirect("/")

	return login_form()
