# -*- coding:utf-8 -*-
from flask import Blueprint,request,jsonify
from flask_login import login_required
from sqlalchemy import literal
from werkzeug.security import generate_password_hash

from wtforms import StringField
from wtforms.validators import DataRequired, length

from modles import User
from exts import db
from common.json_bd import Result,BaseJsonReq
from common.error_code import ConflictException,NotFoundException

user_blueprint = Blueprint("user", __name__, url_prefix="/user")

# 根据id查询用户
@user_blueprint.route('/<int:id>', methods=['GET'])
@login_required
def get_user_info(id):
    user = User.query.get(id)
    if user:
        user_info = {
            'id': user.id,
            'nikename': user.nikename
        }
        return jsonify(Result.ok(user_info))
    else:
        raise NotFoundException(error_code='U-404',msg='用户不存在')

# 新增用户
class AddUserCmd(BaseJsonReq):
    username = StringField(validators=[DataRequired(message='用户名为空'),length(message='用户名允许[5-20]个字符',min=5, max=20)])
    password = StringField(validators=[DataRequired(message='密码为空'),length(message='密码允许[3-20]个字符',min=3, max=20)])
    nikename = StringField(validators=[DataRequired(message='昵称为空'),length(message='昵称允许[1-10]个字符',min=1, max=10)])

@user_blueprint.route('/', methods=['POST'])
@login_required
def add():
    cmd = AddUserCmd().init_and_validate()

    session = db.session
    
    # 查询是否存在
    exists = session.query(literal(True))\
        .filter( User.query.filter_by(username=cmd.username.data).exists()).scalar()

    if exists:
        raise ConflictException(error_code='U-409',msg='用户名已存在')
    
    # 新增
    new_user = User(**cmd.data)
    # 混淆明文
    passwd = generate_password_hash(password=new_user.password)
    new_user.password = passwd

    session.add(new_user)
    # 提交事务
    session.commit()
    return jsonify(Result.ok(data=new_user.id))
