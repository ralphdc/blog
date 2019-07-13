#!/usr/bin/env python3

from flask import render_template, request, make_response,jsonify
from app.models import Visit
from app import app, db, login_required
import datetime
from . import admin



@admin.route('/main', methods=['GET'])
def main_index():

    today_date = datetime.date.today()

    start_time = "{} 00:00:00".format(today_date)
    end_time = "{} 23:59:59".format(today_date)

    visitQuery = db.session.query(Visit.visit_name, Visit.visit_ip, Visit.created_at).filter(Visit.created_at.between(start_time, end_time)).all()

    return render_template('main/index.html', visit=visitQuery)
