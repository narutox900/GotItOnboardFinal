class CustomException(Exception):
    def __init__(self, message, status_code):
        self.body = {'message': message}
        self.status_code = status_code

    def __str__(self):
        return self.body['message']


class BadRequestException(CustomException):
    def __init__(self, message='Bad Request'):
        super().__init__(message, 400)


class AuthenticationException(CustomException):
    def __init__(self, message='Unauthenticated'):
        super().__init__(message, 401)


class AuthorizationException(CustomException):
    def __init__(self, message='Forbidden'):
        super().__init__(message, 403)


class NotFoundException(CustomException):
    def __init__(self, message='Not Found'):
        super().__init__(message, 404)


class DuplicateException(CustomException):
    def __init__(self, message='Duplicated'):
        super().__init__(message, 409)
