#!/usr/bin/env python3

from flask import Blueprint


category = Blueprint('category', __name__)

from .views import *
