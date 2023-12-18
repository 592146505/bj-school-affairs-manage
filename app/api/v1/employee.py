# -*- coding:utf-8 -*-
from flask import Blueprint,jsonify
from flask_login import login_required
from sqlalchemy import literal,or_

from wtforms import IntegerField,StringField
from wtforms.validators import DataRequired,length,number_range

from app.libs.json_bd import Result,BaseReq
from app.libs.error_code import ConflictException
from app.models.employee import Employee
from app.models.department import Department

api = Blueprint("employee", __name__, url_prefix="/employee")

# 查询单个职工详情
@api.route('/<int:id>', methods=['GET'])
@login_required
def get_employee_info(id):
    employee = Employee.query.get_or_404(id, error_code='EMP-404', msg='职工不存在')
    employee_info = {
        'id': employee.id,
        'name': employee.name,
        'alias': employee.alias,
        'department_id': employee.department_id
    }
    return jsonify(Result.ok(employee_info))

# 查询分页职工详情
class EmployeePageQry(BaseReq):
    keyword = StringField(default= '',validators=[length(message='关键字允许[1-10]个字符',max=10)])
    page = IntegerField(validators=[DataRequired(message='当前页码为空'),number_range(message='当前页码最小为1',min=1)])
    per_page = IntegerField(validators=[DataRequired(message='每页大小为空'),number_range(message='每页大小最小为1，最大为100',min=1,max=100)])

@api.route('/page', methods=['GET'])
@login_required
def employee_page():
    qry = EmployeePageQry().init_and_validate()
        
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

# 新增职工
class AddEmployeeCmd(BaseReq):
    name = StringField(validators=[DataRequired(message='姓名为空'),length(message='姓名允许[1-10]个字符',min=1, max=10)])
    alias = StringField(validators=[DataRequired(message='别名为空'),length(message='别名允许[1-10]个字符',min=1, max=10)])
    department_id = IntegerField(validators=[DataRequired(message='部门id为空')])

@api.route('/', methods=['POST'])
@login_required
def add():
    cmd = AddEmployeeCmd().init_and_validate()

    # 查询部门
    Department.query.get_or_404(cmd.department_id.data, error_code='EMP-404', msg='部门不存在')
        
    # 查询别名已存在
    exists = Employee.verifyAlias(alias=cmd.alias.data)
    if exists:
        raise ConflictException(error_code='EMP-409', msg='职工别名重复')
    
    employee_id = Employee.create(**cmd.data)

    return jsonify(Result.ok(data=employee_id))
