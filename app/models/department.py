# -*- coding: UTF-8 -*-
from sqlalchemy import Column,Integer,String,SmallInteger,Index,orm,literal

from app.models.base import BaseModel,db

# 部门
class Department(BaseModel):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 部门名称
    name = Column(String(20), unique=True, nullable=False)
    # 描述
    description = Column(String(255), nullable=False, default='')

    @staticmethod
    def create(name, description):
        '''
        新增员工
        '''
        with db.auto_commit():
            department = Department()
            department.name = name
            department.description = description
            db.session.add(department)
            return department.id

    @staticmethod
    def verifyName(name):
        '''
        验证别名
        '''
        return db.session.query(literal(True))\
        .filter(Department.query.filter_by(name=name).exists()).scalar()