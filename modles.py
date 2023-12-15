from exts import db
from sqlalchemy import Index
from flask_login import UserMixin

# 用户
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户名
    username = db.Column(db.String(50), unique=True, nullable=False)
    # 密码
    password = db.Column(db.String(255), nullable=False)
    # 昵称
    nikename = db.Column(db.String(20), nullable=False)

# 员工
class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 姓名
    name = db.Column(db.String(20), nullable=False)
    # 别名
    alias = db.Column(db.String(20), unique=True, nullable=False, default='')
    # 所属部门
    department_id = db.Column(db.Integer, nullable=False)

employee_name_index = Index('idx_emp_name', Employee.name)

# 部门
class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 部门名称
    name = db.Column(db.String(20), unique=True, nullable=False)
    # 描述
    description = db.Column(db.String(255), nullable=False, default='')

