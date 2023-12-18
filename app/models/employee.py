# -*- coding: UTF-8 -*-
from sqlalchemy import Column,Integer,String,Index,orm,literal,or_

from app.models.base import BaseModel,db
from app.libs.error_code import ConflictException

# 员工
class Employee(BaseModel):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 姓名
    name = Column(String(20), nullable=False)
    # 别名
    alias = Column(String(20), unique=True, nullable=False, default='')
    # 所属部门
    department_id = Column(Integer, nullable=False)
    
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name', 'alias', 'department_id']

    @staticmethod
    def create(name, alias, department_id):
        '''
        新增员工
        '''
        with db.auto_commit():
            employee = Employee()
            employee.name = name
            employee.alias = alias
            employee.department_id = department_id
            db.session.add(employee)
            return employee.id

    @staticmethod
    def verifyAlias(alias):
        '''
        验证别名
        '''
        return db.session.query(literal(True))\
        .filter(Employee.query.filter_by(alias=alias).exists()).scalar()
        

employee_name_index = Index('idx_emp_name', Employee.name)