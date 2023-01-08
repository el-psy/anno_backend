from flask import request
from db import get_db, parse_data


def req_need_key(req, keys):
	for key in keys:
		# if not req[key]:
		if key not in req.keys():
			return {
				'message': f'{key} is required.'
			}, 400

	return None

def need_task_status(taskname, status):
	db = get_db()
	data = db.execute(
		'select status from task where taskname = ?', (taskname, )
	).fetchone()
	db.commit()
	data = parse_data(data)
	if data['status'] != status:
		return {
			'message': f'task status {status} is required.'
		}
	return None

# def req(keys):
# 	def wrapper(func):
# 		def inner_wrapper(*args, **kwargs):
			
# 			req = request.values
# 			for key in keys:
# 			# if not req[key]:
# 				if key not in req.keys():
# 					return {
# 						'message': f'{key} is required.'
# 					}, 400
# 			return func(*args, **kwargs)
# 		return inner_wrapper
# 	return wrapper

# def status(require_status):
# 	def wrapper(func):
# 		def inner_wrapper(*args, **kwargs):
# 			db = get_db()
# 			db.execute(
# 				'select status from task where taskname = ?', (taskname,)
# 			)
# 		return inner_wrapper
# 	return wrapper