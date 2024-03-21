from rest_framework.exceptions import APIException

class MinimumLengthError(APIException):
    status_code = 401
    default_detail = '密码长度太短，至少8位！'
    default_code = 'minimum_length_error'

class UserAttributeSimilarityError(APIException):
    status_code = 402
    default_detail = '密码和用户信息重复度太高！'
    default_code = 'user_attribute_similarity_error'

class CommonPassworError(APIException):
    status_code = 403
    default_detail = '密码太常见！'
    default_code = 'common_password_error'

class NumericPasswordError(APIException):
    status_code = 404
    default_detail = '密码不能是纯数字的！'
    default_code = 'numeric_password_error'

class PasswordResetTokenError(APIException):
    status_code= 405
    default_detail = 'Token错误'
    default_code = 'password_reset_token_error'

class EmailError(APIException):
    status_code= 405
    default_detail = 'Email重复'
    default_code = 'email_error'
