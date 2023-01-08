from flask import ( Blueprint, request, redirect, url_for )
import json
from db import ( get_db, parse_data )
from config import config
from auth import auth
from utils import req_need_key

bp = Blueprint('export', __name__, url_prefix='/export')

@bp.route('/task', methods=['GET', 'POST'])
@auth.login_required(role = ['admin'])
def export():
	req = request.get_json()
	if req_need_key(req, ['task_name', 'export_type']) != None:
		return req_need_key(req, ['task_name', 'export_type'])
	export_type = req['export_type']
	if export_type not in ['all', 'over']:
		return {
			'message':'export_type must be all or over.'
		}, 400
	db = get_db()
	task_name = req['task_name']
	if export_type == 'all':
		data = db.execute(
			'select taskid, letters, annos, overmark from annodata where taskname = ?',
			(task_name,)
		).fetchall()
		db.commit()
		data = parse_data(data)

	if export_type == 'over':
		data = db.execute(
			'select taskid, letters, annos from annodata where taskname = ? and overmark = 1',
			(task_name,)
		).fetchall()
		db.commit()
		data = parse_data(data)
	return {
		'message':'OK',
		'res':data
	}