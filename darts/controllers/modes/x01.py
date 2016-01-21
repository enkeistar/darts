from darts import app
from flask import render_template

@app.route("/games/<int:id>/modes/x01/")
def x01_index(id):
	return "HELLO"

