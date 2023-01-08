from flask import ( Blueprint, request, redirect, url_for )
import json
from db import ( get_db, parse_data )
from config import config
from auth import auth
from utils import req_need_key

from log import logger

bp = Blueprint('task', __name__, url_prefix='/task')

# task_status 
# 1. created
# 2. tags maked
# 3. raw data updated
# 4. distubed
# 5. annoing

task_status_buff = ['created', 'tags maked', 'raw data updated', 'distubed', 'annoing']

@bp.route('/create', methods = ['GET', 'POST'])
@auth.login_required(role=['admin'])
def create_task():
	req = request.get_json()
	need_req = req_need_key(req, ['task_name', 'task_type', 'need_tag', 'task_tags', 'task_data'])
	if need_req != None:
		return need_req
	task_name = req['task_name']
	task_type = req['task_type']
	need_tag = req['need_tag']
	task_tags = req['task_tags']
	task_data = req['task_data']
	db = get_db()
	try:
		db.execute(
			'insert into task (taskname, type, needtag, tags, status) values (?,?,?,?,?)',
			(task_name, task_type, need_tag, task_tags, task_status_buff[2])
		)
		db.commit()
	except db.IntegrityError:
		return {
			'message':f"Taskname {task_name} is already registered.",
		}, 400

	db.execute(
		'delete from annodata where taskname = ?', (task_name,)
	)
	db.commit()

	db_insert_data = []
	for (index, item) in enumerate(task_data):
		# item[id] = index
		db_insert_data.append((task_name, item['id'], item['sen'], item['tag'], 0))
	db.executemany('insert into annodata (taskname, taskid, letters, annos, overmark) values (?, ?, ?, ?, ?)', db_insert_data)
	db.commit()
	return {
		'message':'OK'
	}

@bp.route('/get')
@auth.login_required
def get_task():
	db = get_db()
	data = db.execute(
		'select taskname, type, needtag, tags, status from task'
	).fetchall()
	db.commit()
	data = parse_data(data)
	return {
		'message': data
	}

@bp.route('/base', methods=['GET', 'POST'])
@auth.login_required(role=['admin', 'plain'])
def base():
	req = request.get_json()
	need_req = req_need_key(req, ['task_name'])
	if need_req != None:
		return need_req
	task_name = req['task_name']
	db = get_db()
	data = db.execute('select type, tags from task where taskname = ?', (task_name,)).fetchone()
	db.commit()
	data = parse_data(data)
	return {
		'message':'OK',
		'data': data
	}

@bp.route('/delete', methods = ['GET', 'POST'])
@auth.login_required(role=['admin'])
def delete_task():
	req = request.get_json()

	if req_need_key(req, ['task_name']) != None:
		return req_need_key(req, ['task_name'])

	task_name = req['task_name']
	db = get_db()
	db.execute(
		'delete from task where taskname = ?', (task_name,)
	)
	db.commit()
	db.execute(
		'delete from annodata where taskname = ?', (task_name,)
	)
	db.commit()
	db.execute(
		'delete from distrube where taskname = ?', (task_name,)
	)
	db.commit()
	return {
		'message':'OK'
	}

@bp.route('/dist', methods = ['GET', 'POST'])
@auth.login_required(role=['plain'])
def get_dist_task():
	req = request.get_json()
	need_req = req_need_key(req, ['user_name'])
	if need_req != None:
		return need_req
	user_name = req['user_name']

	db = get_db()
	data = db.execute(
		'select taskname from distrube where username = ?', (user_name, )
	).fetchall()
	db.commit()
	taskname_list = parse_data(data)

	# logger.warn(str(taskname_list))

	res = []

	for taskname in taskname_list:
		taskname = taskname['taskname']
		node = {'taskname': taskname}
		data = db.execute('select count(*) from annodata where taskname = ?', (taskname,)).fetchone()
		db.commit()
		node['all'] = parse_data(data)['count(*)']
		data = db.execute('select count(*) from annodata where taskname = ? and overmark = 1', (taskname,)).fetchone()
		db.commit()
		node['over'] = parse_data(data)['count(*)']
		data = db.execute('select type from task where taskname = ?', (taskname,)).fetchone()
		db.commit()
		node['type'] = parse_data(data)['type']
		res.append(node)
	# logger.warn(str(res))
	return {
		'message': res
	}


# def task_status(task_name):
# 	db = get_db()
# 	data = db.execute(
# 		'select count(*) as c from task where taskname = ?', task_name
# 	)
# 	data = parse_data(data)
# 	if data['c'] == 0:
# 		return {
# 			'message': 'no task'
# 		}
# 	data = db.execute(
# 		'select count(*) as c from distrube where taskname = ?', task_name
# 	)
# 	if data['c'] == 0:
# 		return {
# 			'message': 'register'
# 		}
# 	data = db.execute(
# 		'select count(*) as c from annodata where taskname = ?', task_name
# 	)
# 	if data['c'] == 0:
# 		return {
# 			'message': 'distrubed'
# 		}
# 	return {
# 		'message': 'over'
# 	}