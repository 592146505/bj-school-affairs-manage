# -*- coding:utf-8 -*-

from flask import Flask,jsonify
from flask_migrate import Migrate

from exts import db,login_manager

from blueprints.auth import auth_blueprint
from blueprints.user import user_blueprint
from blueprints.employee import employee_blueprint

from werkzeug.exceptions import HTTPException
from common.error_code import InternalServerErrorException
from common.error import APIException

app = Flask(__name__)
# 绑定配置文件
app.config.from_pyfile('config.py')

# 把db与app绑定
db.init_app(app)

# 上传数据库
migrate = Migrate(app, db)

# 认证管理器
login_manager.init_app(app)

## 注册蓝图
app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(employee_blueprint)

@app.errorhandler(Exception)
def framework_error(error):
    if isinstance(error, APIException):
        return error
    if isinstance(error, HTTPException):
        code = error.code
        msg = error.description
        error_code = str(error.code)
        return APIException(msg, code, error_code)
    else:
        print(error)
        return InternalServerErrorException()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True,)