# -*- coding:utf-8 -*-
from flask import Blueprint,jsonify
from flask_login import login_user,login_required,logout_user
from werkzeug.security import check_password_hash

from exts import login_manager

from wtforms import StringField
from wtforms.validators import DataRequired, length

from modles import User
from common.json_bd import Result,BaseJsonReq
from common.error_code import UnauthorizedException


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

# 用于认证管理器加载用户信息
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 登录
class LoginCmd(BaseJsonReq):
    username = StringField(validators=[DataRequired(message='用户名为空'),length(message='用户名允许[5-20]个字符',min=5, max=20)])
    password = StringField(validators=[DataRequired(message='密码为空'),length(message='密码允许[3-20]个字符',min=3, max=20)])

@auth_blueprint.route('/login', methods=['POST'])
def login():
    cmd = LoginCmd().init_and_validate()
    user = User.query.filter_by(username=cmd.username.data).first()
    if user and check_password_hash(user.password, cmd.password.data):
        login_user(user)
        return jsonify(Result.ok())
    else:
        raise UnauthorizedException(error_code='AUTH-401', msg='用户名或密码错误')

# 登出
@auth_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(Result.ok())