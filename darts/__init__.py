import os
from flask import Flask, request, render_template
app = Flask(__name__)

from darts.controllers import main
from darts.controllers import players
from darts.controllers import games
from darts import HttpMethod

app.register_blueprint(main.mod)
app.register_blueprint(players.mod)
app.register_blueprint(games.mod)

# app.wsgi_app = HttpMethod.HttpMethod(app.wsgi_app)

@app.errorhandler(404)
def not_found(error):
    return render_template("main/404.html"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template("main/500.html"), 500

if __name__ == "__main__":
	app.run(host = "0.0.0.0")
