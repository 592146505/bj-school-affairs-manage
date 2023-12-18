# -*- coding:utf-8 -*-
from flask import Blueprint,jsonify
from flask_login import login_required

from wtforms import StringField
from wtforms.validators import DataRequired, length

from app.libs.json_bd import Result,BaseReq
from app.libs.error_code import ConflictException
from app.models.user import User

api = Blueprint("user", __name__, url_prefix="/user")

# 根据id查询用户
@api.route('/<int:id>', methods=['GET'])
@login_required
def get_user_info(id):
    user = User.query.get_or_404(id, error_code='U-404', msg='用户不存在')
    user_info = {
        'id': user.id,
        'nickname': user.nickname,
    }
    return jsonify(Result.ok(user_info))
    

# 新增用户
class AddUserCmd(BaseReq):
    username = StringField(validators=[DataRequired(message='用户名为空'),length(message='用户名允许[5-20]个字符',min=5, max=20)])
    password = StringField(validators=[DataRequired(message='密码为空'),length(message='密码允许[3-20]个字符',min=3, max=20)])
    nickname = StringField(validators=[DataRequired(message='昵称为空'),length(message='昵称允许[1-10]个字符',min=1, max=10)])

@api.route('/', methods=['POST'])
@login_required
def add():
    cmd = AddUserCmd().init_and_validate()
    # 查询是否存在
    exists = User.verifyUsername(cmd.username.data)
    if exists:
        raise ConflictException(error_code='U-409',msg='用户名已存在')
    # 新增
    user_id = User.register_by_username(nickname=cmd.nickname.data, username=cmd.username.data, password=cmd.password.data)
    
    return jsonify(Result.ok(data=user_id))
