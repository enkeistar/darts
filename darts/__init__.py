import os
from flask import Flask
app = Flask(__name__)

from darts.controllers import main
from darts.controllers import users

app.register_blueprint(main.mod)
app.register_blueprint(users.mod)

if __name__ == "__main__":
	app.run(debug = True, host = "0.0.0.0")
