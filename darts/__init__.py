import os
from flask import Flask, request, render_template, session
from flask.sessions import SessionInterface
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
assets = Environment(app)

from darts.controllers import api
from darts.controllers import brackets
from darts.controllers import matches
from darts.controllers import leaderboard
from darts.controllers import main
from darts.controllers import players
from darts.controllers import mark_styles
from darts.controllers import login

from darts.controllers.modes import cricket
from darts.controllers.modes import x01

session_opts = {
	"session.type": "ext:memcached",
	"session.url": "127.0.0.1:11211",
	"session.data_dir": "./cache"
}

class BeakerSessionInterface(SessionInterface):
	def open_session(self, app, request):
		session = request.environ["beaker.session"]
		return session

	def save_session(self, app, session, response):
		session.save()

@app.errorhandler(404)
def not_found(error):
    return render_template("main/404.html"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template("main/500.html"), 500

@app.after_request
def afterRequest(response):
	model.Model().close()
	return response

if __name__ == "__main__":
	app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
	app.session_interface = BeakerSessionInterface()
	app.run()
