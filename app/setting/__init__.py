#!/usr/bin/env python3

from flask import Blueprint


setting = Blueprint('setting', __name__)

'''
#blueprint add filter;  
@setting.before_request
def restrict_bp_to_admins():
    if not users.is_current_user_admin():
        return redirect(users.create_login_url(request.url))
'''


from . import views