from flask import Flask 

def register_blueprints(app: Flask):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_plugin(app: Flask):
    from app.models.base import db
    from app.exts import login_manager
    db.init_app(app)
    # 认证管理器
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()
        
def register_error_handler(app: Flask):
    from werkzeug.exceptions import HTTPException
    from app.libs.error_code import InternalServerErrorException
    from app.libs.error import APIException
    
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
    
    app.register_error_handler(Exception, framework_error)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    register_blueprints(app)
    register_plugin(app)
    register_error_handler(app)
    
    return app