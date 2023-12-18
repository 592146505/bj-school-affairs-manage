# -*- coding: UTF-8 -*-
from sqlalchemy import Column,Integer,String,SmallInteger,Index,orm,literal
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

from app.models.base import BaseModel,db
from app.libs.error_code import UnauthorizedException

# 用户
class User(UserMixin, BaseModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(20), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    _password = Column("password", String(255), nullable=False)
    auth_scope = Column(SmallInteger, default=0)


    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'username', 'nickname', 'auth_scope']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_username(nickname, username, password):
        '''
        注册用户
        '''
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.username = username
            user.password = password
            db.session.add(user)
            return user.id

    @staticmethod
    def verify(username, password):
        '''
        校验密码
        '''
        user = User.query.filter_by(username=username).first_or_404(error_code='AUTH-401', msg='用户名或密码错误')
        if not user.check_password(password):
            raise UnauthorizedException(error_code='AUTH-401', msg='用户名或密码错误')
        return user
    


    @staticmethod
    def verifyUsername(username):
        return db.session.query(literal(True))\
        .filter(User.query.filter_by(username=username).exists()).scalar()

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)



user_username_index = Index('idx_username', User.username)