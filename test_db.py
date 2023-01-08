import sqlite3
from config import config
import atexit
import os
# import click
# from flask import current_app, g
# from flask.cli import with_appcontext

# def get_db():
# 	if 'db' not in g:
# 		g.db = sqlite3.connect(
# 			current_app.config['DATABASE'],
# 			detect_types=sqlite3.PARSE_DECLTYPES
# 		)
# 		g.db.row_factory = sqlite3.Row

# 	return g.db

# def close_db(e=None):
# 	db = g.pop('db', None)
# 	if db is not None:
# 		db.close()

# def init_db():
# 	db = get_db()
# 	with current_app.open_resource('schema.sql') as f:
# 		db.executescript(f.read().decode('utf-8'))

# @click.command('init-db')
# @with_appcontext
# def init_db_command():
# 	init_db()
# 	click.echo('Initialized the database.')

# def init_app(app):
# 	app.teardown_appcontext(close_db)
# 	app.cli.add_command(init_db_command)

db = None

def get_db():
	global db
	# print(config['database']['path'])
	if not os.path.exists(config['database']['dir']):
		os.makedirs(config['database']['dir'])
	if db == None:
		db = sqlite3.connect(
			config['database']['path'],
			# 'database/db.sqlite',
			detect_types= sqlite3.PARSE_DECLTYPES,
			check_same_thread=False
		)
	db.row_factory = sqlite3.Row
	return db

def parse_data(data):
	if type(data)==list:
		return [parse_data(i) for i in data]
	elif type(data) == sqlite3.Row:
		return {k:data[k] for k in data.keys()}
	else:
		return data

def init_db():
	db = get_db()
	# print(config['database']['path'])
	with open(config['database']['init_script'], 'r', encoding='utf-8') as f:
		db.executescript(f.read())
		db.commit()
		# print(data)
	print('init_db')

@atexit.register
def close_db():
	global db
	if db!=None:
		db.close()
	db = None

if __name__ == '__main__':
	init_db()