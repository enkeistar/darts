from darts import app
from flask import render_template

@app.route("/matches/<int:id>/modes/template/")
def template_index(id):
	return "HELLO"

