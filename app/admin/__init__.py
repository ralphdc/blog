#!/usr/bin/env python3


from flask import Blueprint


admin = Blueprint('admin', __name__)

from . import main

from . import article

from . import module

from . import user

from . import category

from . import comment

from . import album