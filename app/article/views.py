#!/usr/bin/env python3

from flask import request, render_template, jsonify, session

from . import article



@article.route('/')
def article_index():

    return render_template('article/index.html')



@article.route('/add', methods=['POST', 'GET'])
def article_add():


    return render_template('article/add.html')


