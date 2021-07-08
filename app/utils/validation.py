from functools import wraps

from flask import request
from marshmallow import ValidationError

from app.models.item import ItemModel
from app.models.category import CategoryModel
from app.models.user import UserModel
from app.utils.exception import BadRequestException, DuplicateException, AuthorizationException
from app.utils.messages.message import UNAUTHORIZED, USERNAME_DUPLICATED, CATEGORY_DUPLICATED, ITEM_DUPLICATED, \
    LOGGED_IN


def load_and_validate_data(schema):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                data = request.args.to_dict() if request.method == 'GET' else request.get_json()
                data = schema().load(data)
            except ValidationError:
                raise BadRequestException()
            return function(data=data, *args, **kwargs)

        return wrapper

    return decorator


def category_owner_validate(function):
    @wraps(function)
    def decorator(category, user, *args, **kwargs):
        if category.user_id != user.id:
            raise AuthorizationException(UNAUTHORIZED)
        return function(category=category, user=user, *args, **kwargs)

    return decorator


def item_owner_validate(function):
    @wraps(function)
    def decorator(item, user, *args, **kwargs):
        if item.user_id != user.id:
            raise AuthorizationException(UNAUTHORIZED)
        return function(item=item, user=user, *args, **kwargs)

    return decorator


def duplicate_item_name_validate(function):
    @wraps(function)
    def decorator(data, *args, **kwargs):
        if ItemModel.get_item_by_name(data['name']):
            raise DuplicateException(ITEM_DUPLICATED)
        return function(data=data, *args, **kwargs)

    return decorator


def duplicate_category_name_validate(function):
    @wraps(function)
    def decorator(data, *args, **kwargs):
        if CategoryModel.get_category_by_name(data['name']):
            raise DuplicateException(CATEGORY_DUPLICATED)
        return function(data=data, *args, **kwargs)

    return decorator


def duplicate_username_validate(function):
    @wraps(function)
    def decorator(data, *args, **kwargs):
        if UserModel.get_user_by_username(data['username']):
            raise DuplicateException(USERNAME_DUPLICATED)
        return function(data=data, *args, **kwargs)

    return decorator


def logged_in_validate(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        header = request.headers.get('Authorization', None)
        if header:
            raise BadRequestException(LOGGED_IN)
        return function(*args, **kwargs)

    return decorator
