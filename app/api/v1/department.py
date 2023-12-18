# -*- coding:utf-8 -*-
from flask import Blueprint,jsonify
from flask_login import login_required

from wtforms import IntegerField,StringField
from wtforms.validators import DataRequired,length,number_range


from app.models.department import Department
from app.libs.json_bd import Result,BaseReq
from app.libs.error_code import ConflictException

api = Blueprint("department", __name__, url_prefix="/department")

# 查询单个部门详情
@api.route('/<int:id>', methods=['GET'])
@login_required
def get_department_info(id):
    department = Department.query.get_or_404(id, error_code='DEP=404', msg='部门不存在')
    department_info = {
        'id': department.id,
        'name': department.name,
        'description': department.description,
    }
    return jsonify(Result.ok(department_info))

# 分页查询部门详情
class DepartmentPageQry(BaseReq):
    keyword = StringField(default= '',validators=[length(message='关键字最多[20]个字符',max=20)])
    page = IntegerField(validators=[DataRequired(message='当前页码为空'),number_range(message='当前页码最小为1',min=1)])
    per_page = IntegerField(validators=[DataRequired(message='每页大小为空'),number_range(message='每页大小最小为1，最大为100',min=1,max=100)])

@api.route('/page', methods=['GET'])
@login_required
def department_page():
    qry = DepartmentPageQry().init_and_validate()
        
    departments = Department.query\
        .filter(Department.name.ilike(f'%{qry.keyword.data}%')) \
        .paginate(page=qry.page.data, per_page=qry.per_page.data, error_out=False)
    result = {
        'items':[{'id': department.id,'name': department.name,\
                  'description': department.description} for department in departments],
        'paginate':{
            'pages':departments.pages,
            'total':departments.total
         }
     }
    return jsonify(Result.ok(data=result))

# 新增员工
class AddDepartmentCmd(BaseReq):
    name = StringField(validators=[DataRequired(message='部门名称为空'),length(message='部门名称允许[1-20]个字符',min=1, max=20)])
    description = StringField(default='',validators=[length(message='描述最多[250]个字符', max=250)])

@api.route('/', methods=['POST'])
@login_required
def add():
    cmd = AddDepartmentCmd().init_and_validate()
        
    # 查询名称已存在
    exists = Department.verifyName(name=cmd.name.data)
    if exists:
        raise ConflictException(error_code='DEP-409', msg='部门名称重复')
    
    department_id = Department.create(**cmd.data)
    return jsonify(Result.ok(data=department_id))
