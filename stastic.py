from flask import ( Blueprint, request, redirect, url_for )
import json
from db import ( get_db, parse_data )
from config import config
from auth import auth

bp = Blueprint('stastic', __name__, url_prefix='/stastic')

@bp.route('/')
@auth.login_required()
def stastic():
	pass