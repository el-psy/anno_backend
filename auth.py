from flask import ( Blueprint, request, redirect, url_for )
import json
from db import ( get_db, parse_data )
from flask_httpauth import HTTPTokenAuth
from datetime import datetime, timedelta, timezone
import jwt
import secrets
# import time
from config import config

from utils import req_need_key
from log import logger

bp = Blueprint('auth', __name__, url_prefix='/auth')
auth = HTTPTokenAuth(scheme = 'Bearer')

key = None

def create_key():
	global key
	if key == None:
		key = secrets.token_urlsafe(config['auth']['default_secret_length'])
	return key

def create_token(user_name, actor):
	payload = {
		'exp':datetime.now(tz=timezone.utc)+timedelta(seconds=config['auth']['default_token_keep_time']),
		# 'nbf':'',
		'iss':user_name,
		# 'aud':'',
		'actor':actor,
		'iat':datetime.now(tz=timezone.utc)
	}
	key = create_key()
	token = jwt.encode(payload, key, algorithm='HS256')
	return token

@auth.verify_token
def verify_token(token):
	try:
		dec = jwt.decode(token, key, algorithms=['HS256'])
		# logger.warn(dec['actor'])
		return dec['actor']
	except:
		return None

@auth.get_user_roles
def get_roles(buff):
	# logger.warn(buff)
	return buff

@bp.route('/login', methods = ['GET', 'POST'])
def login():
	req = request.get_json()
	need_req = req_need_key(req, ['user_name', 'password'])
	if need_req != None:
		return need_req
	db = get_db()
	data = db.execute(
		'select password as c, actor as a from user where username = ?',
		(req['user_name'],)
	).fetchone()
	data = parse_data(data)

	# logger.warn(str(data))
	if(data == None):
		return {
			'message':'wrong user_name',
		}, 400
	password = data['c']
	if(password == req['password']):
		token = create_token(req['user_name'], data['a'])
		return {
			'set-token':token,
			'message':'OK',
			'actor':data['a']
		}
	else:
		return {
			'message':'wrong password',
		}, 400


@bp.route('/register', methods = ['GET', 'POST'])
def register():
	req = request.get_json()
	need_req = req_need_key(req, ['user_name', 'password'])
	if need_req != None:
		return need_req
	db = get_db()
	data = db.execute(
		'select count(*) as c from user'
	).fetchone()
	user_count = parse_data(data)['c']

	if(user_count==0):
		actor = 'admin'
	else: actor = 'plain'
	# logger.info('actor '+actor)
	try:
		db.execute(
			'insert into user (username, password, actor) values (?, ?, ?) ',
	 		(req['user_name'], req['password'], actor)
		)
		db.commit()
		logger.info('register db insert')
	except db.IntegrityError:
		return {
			'message':f"User {req['user_name']} is already registered.",
		}, 400
	except Exception as e:
		logger.info('register db insert')
		logger.info(str(e))
	return 'OK'

@bp.route('/logout', methods = ['GET', 'POST'])
def logout():
	req = json.loads(request.data)
	# error = None
	# if not req['username']:
	# 	error = 'Username is required.'
	if req_need_key(req, ['user_name']) != None:
		return req_need_key(req, ['user_name'])
	db = get_db()

@bp.route('/get', methods=['POST'])
@auth.login_required(role=['admin'])
def user_get():
	db = get_db()
	data = db.execute('select * from user where actor="plain"').fetchall()
	data = parse_data(data)
	return {
		'message':data
	}