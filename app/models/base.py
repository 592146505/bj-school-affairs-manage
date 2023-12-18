# -*- coding: UTF-8 -*-
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy.query import Query as BaseQuery

from sqlalchemy import inspect, Column, Integer, SmallInteger, orm,SelectBase
from contextlib import contextmanager

from app.libs.error_code import NotFoundException
'''
see: https://github.com/luyuze95/ginger/blob/master/app/models/base.py#L110
'''
class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'deleted' not in kwargs.keys():
            kwargs['deleted'] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident, error_code, msg):
        rv = self.get(ident)
        if not rv:
            raise NotFoundException(error_code=error_code,msg=msg)
        return rv

    def first_or_404(self, error_code, msg):
        rv = self.first()
        if not rv:
            raise NotFoundException(error_code=error_code,msg=msg)
        return rv


db = SQLAlchemy(query_class=Query)


class BaseModel(db.Model):
    __abstract__ = True
    create_time = Column(Integer)
    update_time = Column(Integer)
    deleted = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())
        self.update_time = int(datetime.now().timestamp())

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None
    
    @property
    def update_datetime(self):
        if self.update_time:
            return datetime.fromtimestamp(self.update_time)
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self


class MixinJSONSerializer:
    @orm.reconstructor
    def init_on_load(self):
        self._fields = []
        # self._include = []
        self._exclude = []

        self._set_fields()
        self.__prune_fields()

    def _set_fields(self):
        pass

    def __prune_fields(self):
        columns = inspect(self.__class__).columns
        if not self._fields:
            all_columns = set(columns.keys())
            self._fields = list(all_columns - set(self._exclude))

    def hide(self, *args):
        for key in args:
            self._fields.remove(key)
        return self

    def keys(self):
        return self._fields

    def __getitem__(self, key):
        return getattr(self, key)