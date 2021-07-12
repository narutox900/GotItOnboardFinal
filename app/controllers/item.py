from flask import Blueprint, jsonify

from app.models.item import ItemModel
from app.schemas.item import CreateItemSchema, GetItemSchema
from app.schemas.pagination import PaginationSchema
from app.utils.loader import load_category_by_id, load_item_by_id, dump_schema_decorator
from app.utils.security import token_required
from app.utils.validation import load_and_validate_data, item_owner_validate, duplicate_item_name_validate

category_item_blueprint = Blueprint('category_item_blueprint', __name__, url_prefix='/categories/<category_id>/items')
all_item_blueprint = Blueprint('all_item_blueprint', __name__, url_prefix='/items')


@category_item_blueprint.route('', methods=['POST'])
@token_required
@load_and_validate_data(CreateItemSchema)
@load_category_by_id
@duplicate_item_name_validate
@dump_schema_decorator(GetItemSchema)
def create_item(category, user, data):
    item = ItemModel(**data)
    item.user_id = user.id
    item.category_id = category.id
    item.save()
    return item


@category_item_blueprint.route('/<item_id>', methods=['PUT'])
@token_required
@load_and_validate_data(CreateItemSchema)
@load_category_by_id
@load_item_by_id
@item_owner_validate
@dump_schema_decorator(GetItemSchema)
def update_item(item, data, *args, **kwargs):
    item.update(**data)
    return item


@category_item_blueprint.route('/<item_id>', methods=['DELETE'])
@token_required
@load_category_by_id
@load_item_by_id
@item_owner_validate
def delete_item(item, *args, **kwargs):
    item.delete()
    return jsonify(message='Deleted'), 200


@category_item_blueprint.route('/<item_id>', methods=['GET'])
@load_category_by_id
@load_item_by_id
@dump_schema_decorator(GetItemSchema)
def get_item_by_id(item, *args, **kwargs):
    return item


@category_item_blueprint.route('', methods=['GET'])
@load_and_validate_data(PaginationSchema)
@load_category_by_id
@dump_schema_decorator(GetItemSchema, True)
def get_items(category, data):
    items = ItemModel.get_items_by_category_id(category_id=category.id, page=data['page'], limit=data['limit'])
    return {'items': items, 'total': ItemModel.get_category_items_number(category.id),
            'limit': data['limit']}


@all_item_blueprint.route('', methods=['GET'])
@load_and_validate_data(PaginationSchema)
@dump_schema_decorator(GetItemSchema, True)
def get_latest_items(data):
    return {'items': ItemModel.get_latest_items(data['page'], data['limit']),
            'total': ItemModel.get_total_items_number(), 'limit': data['limit']}
