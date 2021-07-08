from flask import Blueprint, jsonify

from app.models.item import ItemModel
from app.schemas.item import CreateItemSchema, GetItemSchema
from app.schemas.pagination import PaginationSchema
from app.utils.loader import load_category_by_id, load_item_by_id
from app.utils.security import token_required
from app.utils.validation import load_and_validate_data, item_owner_validate, duplicate_item_name_validate

category_item_blueprint = Blueprint('category_item_blueprint', __name__, url_prefix='/categories/<category_id>/items')
all_item_blueprint = Blueprint('all_item_blueprint', __name__, url_prefix='/items')


@category_item_blueprint.route('', methods=['POST'])
@token_required
@load_and_validate_data(CreateItemSchema)
@load_category_by_id
@duplicate_item_name_validate
def create_item(category, user, data):
    item = ItemModel(**data)
    item.user_id = user.id
    item.category_id = category.id
    item.save()
    return jsonify(dump_item(item)), 200


@category_item_blueprint.route('/<item_id>', methods=['PUT'])
@token_required
@load_and_validate_data(CreateItemSchema)
@load_category_by_id
@load_item_by_id
@item_owner_validate
def update_item(item, data, *args, **kwargs):
    item.update(**data)
    return jsonify(dump_item(item)), 200


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
def get_item_by_id(item, *args, **kwargs):
    return jsonify(dump_item(item)), 200


@category_item_blueprint.route('', methods=['GET'])
@load_and_validate_data(PaginationSchema)
@load_category_by_id
def get_items(category, data):
    items = ItemModel.get_items_by_category_id(category_id=category.id, page=data['page'], limit=data['limit'])
    return jsonify(items=dump_item(items, many=True), total=ItemModel.get_category_items_number(category.id),
                   limit=data['limit']), 200


@all_item_blueprint.route('', methods=['GET'])
@load_and_validate_data(PaginationSchema)
def get_latest_items(data):
    return jsonify(items=dump_item(ItemModel.get_latest_items(data['page'], data['limit']), many=True),
                   total=ItemModel.get_total_items_number(), limit=data['limit']), 200


def dump_item(item, many=False):
    return GetItemSchema(many=many).dump(item)
