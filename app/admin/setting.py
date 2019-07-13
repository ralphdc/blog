#!/usr/bin/env python3

from flask import render_template, request, make_response, jsonify
from app import app
from app.mongo import mongodb
from . import admin


@admin.route('/setting', methods=['GET'])
def basicset_index():

    collection = app.config.get('BASICSET_COLLECTION')

    setting = mongodb[collection].find_one({"usageTag":"blog_setting"})

    if setting:
        blog_title          = setting.get('blog_title')
        blog_keywords       = setting.get('blog_keywords')
        blog_description    = setting.get('blog_description')
        blog_tag            = setting.get('blog_tag')



    return render_template('setting/index.html')