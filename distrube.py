from flask import ( Blueprint, request, redirect, url_for )
import json
from db import ( get_db, parse_data )
from config import config
from auth import auth
from utils import req_need_key


bp = Blueprint('distrube', __name__, url_prefix='/distrube')

@bp.route('/all', methods = ['GET', 'POST'])
@auth.login_required(role=['admin'])
def get_all_dist():
	db = get_db()
	data = db.execute('select * from distrube').fetchall()
	db.commit()
	data = parse_data(data)
	return {
		'message':data
	}

@bp.route('/set', methods = ['GET', 'POST'])
@auth.login_required(role=['admin'])
def set_dist():
	req = request.get_json()
	need_req = req_need_key(req, ['task_name', 'users'])
	if need_req != None:
		return need_req
	task_name = req['task_name']
	users = req['users']

	users = set(users)
	dist_buff_list = []
	for user in users:
		dist_buff_list.append((task_name, user, ''))

	db = get_db()
	db.execute(
		'delete from distrube where taskname = ?', (task_name,)
	)
	db.commit()
	db.executemany(
		'insert into distrube (taskname, username, dist) values (?, ?, ?)', dist_buff_list
	)
	db.commit()
	return {
		'message':'OK'
	}

	# req = request.get_json()
	# need_req = req_need_key(req, ['task_name', 'dist_data'])
	# if need_req != None:
	# 	return need_req
	# task_name = req['task_name']
	# dist_data = req['dist_data']

	# # dist_data
	# # {
	# # 	"user_name":
	# # 	"tags":
	# # 	"id_range":
	# # }

	# dist_buff_list = []
	# for dist_node in dist_data:
	# 	buff = {}
	# 	try:
	# 		user_name = dist_node['user_name']
	# 		buff['tags'] = dist_node['tags']
	# 		buff['idrange'] = dist_node['id_range']
	# 		dist_buff_list.append((task_name, user_name, (json.dumps(buff, ensure_ascii=False))))
	# 	except Exception as e:
	# 		return {
	# 			'message':'dist_data structure is error',
	# 			'error_str': str(e)
	# 		}, 400
	
	# db = get_db()
	# db.execute(
	# 	'delete from distrube where taskname = ?', (task_name,)
	# )
	# db.commit()
	# db.executemany(
	# 	'insert into distrube (taskname, username, dist) values (?, ?, ?)', dist_buff_list
	# )
	# db.commit()
	# return {
	# 	'message':'OK'
	# }