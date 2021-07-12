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


def dump_schema_decorator(schema, many=False):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            ret_val = function(*args, **kwargs)
            ret_dict = {}
            if type(ret_val) is dict:
                for key, value in ret_val.items():
                    if type(value) is list:
                        ret_dict[key] = schema(many=many).dump(value)
                    else:
                        ret_dict[key] = value
            else:
                ret_dict = schema(many=many).dump(ret_val)

            return ret_dict

        return wrapper

    return decorator
