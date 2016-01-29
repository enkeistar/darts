from darts import app
app.config["DEBUG"] = False
app.config["PORT"] = 5000
app.config.from_pyfile("config_file.cfg")
app.run(debug = app.config["DEBUG"], host = "0.0.0.0", port = app.config["PORT"])