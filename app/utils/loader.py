from functools import wraps

from app.models.category import CategoryModel
from app.models.item import ItemModel
from app.utils.exception import NotFoundException
from app.utils.messages.message import ITEM_NOT_FOUND, CATEGORY_NOT_FOUND


def load_item_by_id(function):
    @wraps(function)
    def decorator(item_id, category, *args, **kwargs):
        item = ItemModel.get_item_by_id(item_id, category.id)
        if not item:
            raise NotFoundException(ITEM_NOT_FOUND)
        return function(item=item, category=category, *args, **kwargs)

    return decorator


def load_category_by_id(function):
    @wraps(function)
    def decorator(category_id, *args, **kwargs):
        category = CategoryModel.get_category_by_id(category_id)
        if not category:
            raise NotFoundException(CATEGORY_NOT_FOUND)
        return function(category=category, *args, **kwargs)

    return decorator


def dump_schema_decorator(schema):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return schema().dump(function(*args, **kwargs))

        return wrapper

    return decorator
