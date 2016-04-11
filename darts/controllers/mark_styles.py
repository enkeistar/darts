from darts import app
from flask import Response, request, render_template, redirect
from darts.entities import mark_style as markStyleModel
from darts import model
from sqlalchemy.sql.expression import func
from sqlalchemy import desc
from datetime import datetime
from darts.entities import mailer

@app.route("/mark-styles/")
def mark_styles_index():
	admin = False
	if request.remote_addr == "10.9.1.207":
		admin = True

	markStyles = model.Model().select(markStyleModel.MarkStyle).order_by(desc("createdAt"))
	if not admin:
		markStyles = markStyles.filter_by(approved = 1)

	dates = {}
	for markStyle in markStyles:
		dates[markStyle.id] = "{:%b %d, %Y} ".format(markStyle.createdAt)

	return render_template("markstyles/index.html", markStyles = markStyles, dates = dates, admin = admin)

@app.route("/mark-styles/new/")
def mark_styles_new():
	return render_template("markstyles/form.html")

@app.route("/mark-styles/", methods = ["POST"])
def mark_styles_create():
	name = request.form["name"]
	one = request.form["one"].replace('width="320" height="240"', 'viewBox="0 0 320 240"')
	two = request.form["two"].replace('width="320" height="240"', 'viewBox="0 0 320 240"')
	three = request.form["three"].replace('width="320" height="240"', 'viewBox="0 0 320 240"')

	newMarkStyle = markStyleModel.MarkStyle(name, one, two, three, 0, datetime.now())
	model.Model().create(newMarkStyle)

	mailer.Mailer().send("A new mark style has been submitted.", "A new mark style has been submitted by " + name + " for your review.\nIt may be approved or rejected here: http://10.10.0.130:5000/mark-styles/." )

	return redirect("/mark-styles/")

@app.route("/mark-styles/<int:id>/approve/", methods = ["POST"])
def mark_styles_approve(id):
	model.Model().update(markStyleModel.MarkStyle, id, { "approved": 1 })
	return redirect("/mark-styles/")

@app.route("/mark-styles/<int:id>/reject/", methods = ["POST"])
def mark_styles_reject(id):
	model.Model().update(markStyleModel.MarkStyle, id, { "approved": 0 })
	return redirect("/mark-styles/")

@app.route("/mark-styles/<int:id>/delete/", methods = ["POST"])
def mark_styles_delete(id):
	model.Model().delete(markStyleModel.MarkStyle, id)
	return redirect("/mark-styles/")

@app.route("/mark-styles/<int:id>/<path:num>.svg")
def mark_styles_svg(id, num):

	markStyle = model.Model().selectById(markStyleModel.MarkStyle, id)

	if num == "one":
		style = markStyle.one
	elif num == "two":
		style = markStyle.two
	else:
		style = markStyle.three

	return Response(style, mimetype = "image/svg+xml")

