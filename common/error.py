from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'Internal Server Error'
    error_code = '500'

    def __init__(self, msg: str | None=None, code: int | None=None, error_code: str | None=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None,scope=None):
        body = dict(
            code=self.error_code,
            msg=self.msg,
            data=None,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None,scope=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]