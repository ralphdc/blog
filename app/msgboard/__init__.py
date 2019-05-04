#!/usr/bin/env python3


#留言板；
from flask import Blueprint


msgboard = Blueprint('msgboard', __name__)

from . import views

