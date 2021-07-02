from functools import wraps

from flask import request
from marshmallow import ValidationError


def load_and_validate_data(schema):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                data = request.args.to_dict() if request.method == 'GET' else request.get_json()
                data = schema().load(data)
            except ValidationError as e:
                return
            return function(data=data, *args, **kwargs)

        return wrapper

    return decorator


def owner_validate(function):
    @wraps(function)
    def decorator(item, user, *args, **kwargs):
        if item.user_id != user.id:
            pass
        return function(item=item, user=user, *args, **kwargs)
    return decorator
