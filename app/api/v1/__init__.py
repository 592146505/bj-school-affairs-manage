# -*- coding:utf-8 -*-
from flask import Blueprint
from app.api.v1 import auth, user, employee, department

def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__, url_prefix="/v1")

    bp_v1.register_blueprint(auth.api)
    bp_v1.register_blueprint(user.api)
    bp_v1.register_blueprint(employee.api)
    bp_v1.register_blueprint(department.api)
    return bp_v1
    
