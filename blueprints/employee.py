# -*- coding:utf-8 -*-
from flask import Blueprint,jsonify
from flask_login import login_required
from sqlalchemy import literal,or_

from wtforms import IntegerField,StringField
from wtforms.validators import DataRequired,length,number_range

from exts import db

from modles import Employee
from common.json_bd import Result,BaseJsonReq
from common.error_code import ConflictException,NotFoundException


employee_blueprint = Blueprint('employee', __name__, url_prefix='/employee')

# 查询单个员工详情
@employee_blueprint.route('/<int:id>', methods=['GET'])
@login_required
def get_employee_info(id):
    employee = Employee.query.get(id)
    if employee:
        employee_info = {
            'id': employee.id,
            'name': employee.name,
            'alias': employee.alias,
            'department_id': employee.department_id
        }
        return jsonify(Result.ok(employee_info))
    else:
        raise NotFoundException(error_code='EMP-404', msg='员工不存在')

# 查询单个员工详情
class FilterEmployeeQry(BaseJsonReq):
    keyword = StringField(default= '',validators=[length(message='关键字允许[1-10]个字符',max=10)])
    page = IntegerField(validators=[DataRequired(message='当前页码为空'),number_range(message='当前页码最小为1',min=1)])
    per_page = IntegerField(validators=[DataRequired(message='每页大小为空'),number_range(message='每页大小最小为1，最大为100',min=1,max=100)])

@employee_blueprint.route('/filter', methods=['GET'])
@login_required
def filter_employee_info():
    qry = FilterEmployeeQry().init_and_validate()
        
    employees = Employee.query\
        .filter(or_(Employee.name.ilike(f'%{qry.keyword.data}%'), Employee.alias.ilike(f'%{qry.keyword.data}%'))) \
        .paginate(page=qry.page.data, per_page=qry.per_page.data, error_out=False)
    result = {
        'items':[{'id': employee.id,'name': employee.name,'alias'\
               : employee.alias,'department_id': employee.department_id} for employee in employees],
        'paginate':{
            'pages':employees.pages,
            'total':employees.total
         }
     }
    return jsonify(Result.ok(data=result))

# 新增员工
class AddEmployeeCmd(BaseJsonReq):
    name = StringField(validators=[DataRequired(message='姓名为空'),length(message='姓名允许[1-10]个字符',min=1, max=10)])
    alias = StringField(validators=[DataRequired(message='别名为空'),length(message='别名允许[1-10]个字符',min=1, max=10)])
    department_id = IntegerField(validators=[DataRequired(message='部门id为空')])

@employee_blueprint.route('/', methods=['POST'])
@login_required
def add():
    cmd = AddEmployeeCmd().init_and_validate()
    
    session = db.session
    
    # 查询别名已存在
    exists = session.query(literal(True))\
        .filter( Employee.query.filter_by(alias=cmd.alias.data).exists()).scalar()
    if exists:
        raise ConflictException(error_code='EMP-409', msg='员工别名重复')
    
    # TODO 查询部门
    ok = True  
    if not ok:
        return NotFoundException(error_code='EMP-404', msg='部门不存在')
   
    
    new_employee = Employee(**cmd.data)
    session.add(new_employee)
    # 提交事务
    session.commit()
    return jsonify(Result.ok(data=new_employee.id))
