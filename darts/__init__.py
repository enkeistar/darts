import os
from flask import Flask, request, render_template
app = Flask(__name__)

from darts.controllers import main
from darts.controllers import players
from darts import HttpMethod

app.register_blueprint(main.mod)
app.register_blueprint(players.mod)

# app.wsgi_app = HttpMethod.HttpMethod(app.wsgi_app)

@app.errorhandler(404)
def not_found(error):
    return render_template("main/404.html"), 404

if __name__ == "__main__":
	app.run(debug = True, host = "0.0.0.0")
