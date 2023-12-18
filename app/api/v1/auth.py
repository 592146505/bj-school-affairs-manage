# -*- coding:utf-8 -*-
from flask import Blueprint,jsonify
from flask_login import login_user,login_required,logout_user

from app.exts import login_manager

from wtforms import StringField
from wtforms.validators import DataRequired, length

from app.models.user import User
from app.libs.json_bd import Result,BaseReq


api = Blueprint("auth", __name__, url_prefix="/auth")

# 用于认证管理器加载用户信息
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 登录
class LoginCmd(BaseReq):
    username = StringField(validators=[DataRequired(message='用户名为空'),length(message='用户名允许[5-20]个字符',min=5, max=20)])
    password = StringField(validators=[DataRequired(message='密码为空'),length(message='密码允许[3-20]个字符',min=3, max=20)])

@api.route('/login', methods=['POST'])
def login():
    cmd = LoginCmd().init_and_validate()
    user = User.verify(username=cmd.username.data, password=cmd.password.data)
    
    login_user(user)
    return jsonify(Result.ok())

# 登出
@api.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(Result.ok())