from flask import Flask
from flask_cors import CORS
from config import config

def create_app():
	from flask.logging import default_handler

	app = Flask(__name__)
	CORS(app, **(config['cors']))

	app.logger.removeHandler(default_handler)

	from db import init_app
	init_app(app)

	import auth
	app.register_blueprint(auth.bp)

	import anno
	app.register_blueprint(anno.bp)

	import export
	app.register_blueprint(export.bp)

	import stastic
	app.register_blueprint(stastic.bp)

	import task
	app.register_blueprint(task.bp)

	import distrube
	app.register_blueprint(distrube.bp)

	return app
# @app.route('/')
# def hello():
# 	return 'Hello, World!'

if __name__ == '__main__':
	app = create_app()
	app.run(debug=True, port='5000')