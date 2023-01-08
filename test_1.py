from datetime import datetime, timedelta, timezone
import jwt
import secrets
import time

header = {

}
payload = {
	'exp':datetime.now(tz=timezone.utc)+timedelta(seconds=30),
	# 'nbf':'',
	'iss':'admin',
	# 'aud':'',
	'actor':'plain',
	'iat':datetime.now(tz=timezone.utc)
}
key = secrets.token_urlsafe(32)

token = jwt.encode(payload, key, algorithm='HS256')
print(token)
dec = jwt.decode(token, key, algorithms=['HS256'])
print(dec)

def req_need_key(req, keys):
	for key in keys:
		if not req[key]:
			return {
				'message': f'{key} is required.'
			}, 400

	return None

if __name__ == '__main__':
	print(key)
	req = {}
	print(req_need_key(req, ['user_name', 'password']))