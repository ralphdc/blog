#!/usr/bin/env python3

from flask import render_template, request, make_response,jsonify
from flask_login import login_required, current_user
from app.models import Visit
from app import app, db
import datetime
from . import main




@main.route('/', methods=['GET'])
@login_required
def main_index():

    today_date = datetime.date.today()

    start_time = "{} 00:00:00".format(today_date)
    end_time = "{} 23:59:59".format(today_date)

    visitQuery = db.session.query(Visit.visit_name, Visit.visit_ip, Visit.created_at).filter(Visit.created_at.between(start_time, end_time)).all()

    return render_template('main/index.html', visit=visitQuery)
