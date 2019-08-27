#!/usr/bin/env python3

from flask import Blueprint

blog = Blueprint('blog', __name__)

from . import msgboard
from . import index