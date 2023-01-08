from flask import ( Blueprint, request, redirect, url_for )
import json
from db import ( get_db, parse_data )
from config import config
from auth import auth
from utils import req_need_key
from log import logger


bp = Blueprint('anno', __name__, url_prefix='/anno')

# @bp.route('/get')
# @auth.login_required(role=['plain'])
# def get_anno_data():
# 	req = request.values
# 	if req_need_key(req, ['user_name', 'task_name']) != None:
# 		return req_need_key(req, ['user_name', 'task_name'])
# 	db = get_db()
# 	task_name = req['task_name']
# 	user_name = req['user_name']
# 	dist = db.execute(
# 		'select dist from distrube where taskname = ? and username = ?',
# 		(task_name, user_name)
# 	)
# 	dist = parse_data(dist)['dist']
# 	dist = json.loads(dist)
# 	res = []
# 	for node in dist:
# 		data = db.execute(
# 			'select (task_name, task_id, letters, annos) from annodata where task_name = ?', (task_name)
# 		).fetchall()
# 		data = parse_data(data)
# 		res = res + data
# 	return {
# 		'message':'OK',
# 		'anno_data':res
# 	}

@bp.route('/get', methods=['GET', 'POST'])
@auth.login_required(role=['admin', 'plain'])
def get_anno_data():
	req = request.get_json()
	need_req = req_need_key(req, ['task_name'])
	if need_req != None:
		return need_req
	
	task_name = req['task_name']

	db = get_db()
	data = db.execute(
		'select taskname, taskid, letters, annos, overmark from annodata where taskname = ?', (task_name,)
	).fetchall()
	db.commit()
	data = parse_data(data)
	return {
		'message':'OK',
		'anno_data':data
	}

@bp.route('/set', methods = ['GET', 'POST'])
@auth.login_required
def set_data():
	req = request.get_json()
	need_req = req_need_key(req, ['task_name', 'anno_data'])
	if need_req != None:
		return need_req
	task_name = req['task_name']
	anno_data = req['anno_data']
	task_id_buff = {}
	update_data = []
	# logger.warn(str(anno_data))
	try:
		for anno in anno_data:
			task_id_buff[anno['task_id']] = task_id_buff.get(anno['task_id'], 0)
			update_data.append(
				(anno['data'], anno['over_mark'], task_name, anno['task_id'])
			)
			if task_id_buff[anno['task_id']] > 1:
				return {
					'message': f'task_id {anno["task_id"]} should be unique.'
				}, 400
	except Exception as e:
		return {
			'message':'anno_data structure error ?',
			'error_str':str(e)
		}, 400

	db = get_db()
	db.executemany(
		'update annodata set annos = ?, overmark = ? where taskname = ? and taskid = ?',
		update_data
	)
	db.commit()

	return {
		'message':'OK'
	}


@bp.route('/raw', methods=['GET', 'POST'])
@auth.login_required(role=['admin'])
def set_raw_data():
	req = request.get_json()

	need_req = req_need_key(req, ['task_name', 'anno_data'])
	if need_req != None:
		return need_req
	task_name = req['task_name']
	anno_data = req['anno_data']
	task_id_buff = {}
	try:
		for anno in anno_data:
			task_id_buff[anno['task_id']] = task_id_buff.get(anno['task_id'], 0)
			if task_id_buff[anno['task_id']] > 1:
				return {
					'message': f'task_id {anno["task_id"]} should be unique.'
				}, 400
			anno['letters']
	except Exception as e:
		return {
			'message':'anno_data structure error ?',
			'error_str':str(e)
		}, 400
	db = get_db()
	db.execute(
		'delete from annodata where taskname = ?', (task_name,)
	)
	db.commit()
	db_insert_data = []
	for anno in anno_data:
		db_insert_data.append((task_name, anno['task_id'], anno['letters'], '[]', 0))
	db.executemany('insert into annodata (taskname, taskid, letters, annos, overmark) values (?, ?, ?, ?, ?)', db_insert_data)
	db.commit()
	return {
		'message':'OK'
	}