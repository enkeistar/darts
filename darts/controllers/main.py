from darts import app
from flask import Blueprint, render_template

@app.route("/")
def main_index():
	return render_template("main/index.html")

