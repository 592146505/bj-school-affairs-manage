from app.libs.error import APIException

class ParameterException(APIException):
    code = 400
    msg = 'Bad Request'
    error_code = '400'

class UnauthorizedException(APIException):
    code = 401
    msg = 'Unauthorized'
    error_code = '401'

class ForbiddenException(APIException):
    code = 403
    msg = 'Forbidden'
    error_code = '403'

class NotFoundException(APIException):
    code = 404
    msg = 'Not Found'
    error_code = '404'

class MethodNotAllowedException(APIException):
    code = 405
    msg = 'Method Not Allowed'
    error_code = '405'

class NotAcceptableException(APIException):
    code = 406
    msg = 'Not Acceptable'
    error_code = '406'

class ConflictException(APIException):
    code = 409
    msg = 'Conflict'
    error_code = '409'

class UnsupportedMediaTypeException(APIException):
    code = 415
    msg = 'Unsupported Media Type'
    error_code = '415'

class InternalServerErrorException(APIException):
    code = 500
    msg = 'Internal Server Error'
    error_code = '500' 
    