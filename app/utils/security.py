from _datetime import datetime, timedelta
from functools import wraps

import flask
import jwt

from app.config import config
from app.models.user import UserModel
from app.utils.exception import AuthenticationException
from app.utils.messages.message import INVALID_TOKEN, MISSING_TOKEN


def encode_token(payload):
    payload = {**payload, 'iss': 'app', 'iat': datetime.utcnow(), 'exp': datetime.utcnow() + timedelta(days=1)}
    return jwt.encode(payload, config.Config.SECRET_KEY)


def decode_token(token):
    try:
        payload = jwt.decode(token, config.Config.SECRET_KEY, algorithms='HS256')
    except jwt.PyJWTError:
        raise AuthenticationException(INVALID_TOKEN)
    return payload


def token_required(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        header = flask.request.headers.get('Authorization', None)
        if not header:
            raise AuthenticationException(MISSING_TOKEN)
        header = header.split()
        if len(header) != 2 or header[0] != 'Bearer':
            raise AuthenticationException(INVALID_TOKEN)

        payload = decode_token(header[1])
        user = UserModel.get_user_by_id(payload['uid'])
        if not user:
            raise AuthenticationException(INVALID_TOKEN)

        return function(user=user, *args, **kwargs)

    return decorator
