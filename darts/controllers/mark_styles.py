from darts import app
from flask import Response, request, render_template, redirect, session
from darts.entities import mark_style as markStyleModel
from darts import model
from sqlalchemy.sql.expression import func

@app.route("/mark-styles/")
def mark_styles_index():

	print(session.has_key("authenticated"))


	markStyles = model.Model().select(markStyleModel.MarkStyle).filter_by(approved = 1)
	return render_template("markstyles/index.html", markStyles = markStyles)

@app.route("/mark-styles/new/")
def mark_styles_new():
	return render_template("markstyles/form.html")

@app.route("/mark-styles/", methods = ["POST"])
def mark_styles_create():
	one = request.form["one"].replace('width="320" height="240"', 'viewBox="0 0 320 240"')
	two = request.form["two"].replace('width="320" height="240"', 'viewBox="0 0 320 240"')
	three = request.form["three"].replace('width="320" height="240"', 'viewBox="0 0 320 240"')

	newMarkStyle = markStyleModel.MarkStyle(one, two, three, 0)
	model.Model().create(newMarkStyle)
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

