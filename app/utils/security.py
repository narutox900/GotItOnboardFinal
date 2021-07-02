from _datetime import datetime, timedelta
from functools import wraps

import flask
import jwt

from app.config import config
from app.models.user import UserModel


def encode_token(payload):
    payload = {**payload, 'iss': 'app', 'iat': datetime.utcnow(), 'exp': datetime.utcnow() + timedelta(days=1)}
    return jwt.encode(payload, config.Config.SECRET_KEY)


def decode_token(token):
    return jwt.decode(token, config.Config.SECRET_KEY)


def token_required(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        header = flask.request.headers.get('Authorization', None)
        if not header:
            return
        if len(header) != 2:
            return
        if header[0] != 'Bearer':
            return

        try:
            payload = decode_token(header[1])
            user = UserModel.get_user_by_username(payload['aud'])
            if not user:
                raise jwt.PyJWTError

        except jwt.PyJWTError:
            return
        return function(user=user, *args, **kwargs)

    return decorator
