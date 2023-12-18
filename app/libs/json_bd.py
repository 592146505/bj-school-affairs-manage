#coding:utf-8
from wtforms import Form
import wtforms_json
from flask import request
from app.libs.error_code import ParameterException

class BaseReq(Form):
    @classmethod
    def init_and_validate(cls):
        def form_or_json():
            if request.get_json(silent=True):
                return request.get_json(silent=True)
            else:
                if request.form:
                    return request.form
                else:
                    return request.args.to_dict()

        wtforms_json.init()
        form = cls.from_json(form_or_json())
        valid = form.validate()
        if not valid:
            '''
            得到的错误是这种形式的，为了只显示一条字符，决定随机取第一个
            {'username': ['用户名允许[5-20]个字符'], 'nickname': ['昵称为空']}
            '''
            raise ParameterException(msg=next(iter(form.errors.values()), None)[0])
        return form

class Result():
    def __init__(self, data, code, msg):
        self.data = data
        self.code = code
        self.msg = msg

    @classmethod
    def ok(cls, data=None, code='200', msg='ok'):
        return cls(data, code, msg).__dict__

    @classmethod
    def err(cls, data=None, code='500', msg='error'):
        return cls(data, code, msg).__dict__