import sqlite3
from config import config
import os
from flask import g

def get_db():
	# print(config['database']['path'])
	if not os.path.exists(config['database']['dir']):
		os.makedirs(config['database']['dir'])
	db = getattr(g, 'db', None)
	if db == None:
		db = g.db = sqlite3.connect(
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

def close_db(e=None):
	db = g.pop('db', None)
	if db is not None:
		db.close()

def init_app(app):
	app.teardown_appcontext(close_db)

def init_db():
	db = sqlite3.connect(
			config['database']['path'],
			# 'database/db.sqlite',
			detect_types= sqlite3.PARSE_DECLTYPES,
			check_same_thread=False
		)
	# print(config['database']['path'])
	with open(config['database']['init_script'], 'r', encoding='utf-8') as f:
		db.executescript(f.read())
		db.commit()
		# print(data)
	print('init_db')


if __name__ == '__main__':
	init_db()