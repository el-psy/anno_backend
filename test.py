from flask import Flask, redirect, request
from flask_httpauth import HTTPTokenAuth
from datetime import datetime, timedelta, timezone
import jwt
import secrets
import time
from config import config
import json

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

key = None


def create_key():
	global key
	if key == None:
		key = secrets.token_urlsafe(config['auth']['default_secret_length'])
	return key


def create_token(user_id):
	payload = {
		'exp':datetime.now(tz=timezone.utc)+timedelta(seconds=config['auth']['default_token_keep_time']),
		# 'nbf':'',
		'iss':user_id,
		# 'aud':'',
		'actor':'plain',
		'iat':datetime.now(tz=timezone.utc)
	}
	key = create_key()
	token = jwt.encode(payload, key, algorithm='HS256')
	return token

@auth.verify_token
def verify_token(token):
	try:
		dec = jwt.decode(token, key, algorithms=['HS256'])
		return dec['actor']
	except:
		return None


@app.route('/index', methods = ['GET', 'POST'])
@auth.login_required
def index():
	return "Hello, {}!".format(auth.current_user())

@app.route('/login', methods = ['GET','POST'])
def login():
	# print(request.data)
	user_id = request.values['user_id']
	token = create_token(user_id)
	return {
		'set-token': token,
		'secret': create_key(),
		'user_id': user_id
	}

if __name__ == '__main__':
	app.run(port=5700)