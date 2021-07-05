from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError

from app.models.item import ItemModel
from app.utils.security import token_required
from app.utils.validation import load_and_validate_data, item_owner_validate, duplicate_item_name_validate
from app.schemas.item import CreateItemSchema, GetItemSchema
from app.schemas.pagination import PaginationSchema
from app.utils.loader import load_category_by_id, load_item_by_id
from app.utils.exception import DuplicateException

item_blueprint = Blueprint('item_blueprint', __name__, url_prefix='/categories/<category_id>/items')
all_item_blueprint = Blueprint('all_item_blueprint', __name__, url_prefix='/items')


@item_blueprint.route('', methods=['POST'])
@token_required
@load_and_validate_data(CreateItemSchema)
@load_category_by_id
@duplicate_item_name_validate
def create_item(category, user, data):
    item = ItemModel(**data)
    item.user_id = user.id
    item.category_id = category.id
    item.save()
    return jsonify(item=GetItemSchema().dump(item)), 200


@item_blueprint.route('/<item_id>', methods=['PUT'])
@token_required
@load_and_validate_data(CreateItemSchema)
@load_category_by_id
@load_item_by_id
@item_owner_validate
def update_item(item, category, user, data):
    item.update(**data)
    return jsonify(item=GetItemSchema().dump(item)), 200


@item_blueprint.route('/<item_id>', methods=['DELETE'])
@token_required
@load_category_by_id
@load_item_by_id
@item_owner_validate
def delete_item(item, category, user):
    item.delete()
    return jsonify(message='Deleted'), 200


@item_blueprint.route('/<item_id>', methods=['GET'])
@load_category_by_id
@load_item_by_id
def get_item_by_id(item, category):
    return jsonify(items=GetItemSchema().dump(item)), 200


@item_blueprint.route('', methods=['GET'])
@load_and_validate_data(PaginationSchema)
@load_category_by_id
def get_items_by_category_id(category, data):
    items = ItemModel.get_items_by_category_id(category_id=category.id, page=data['page'], limit=data['limit'])
    return jsonify(items=GetItemSchema(many=True).dump(items), total=len(category.items)), 200


@all_item_blueprint.route('', methods=['GET'])
@load_and_validate_data(PaginationSchema)
def get_items_sorted(data):
    return jsonify(items=GetItemSchema(many=True).dump(ItemModel.get_items_sorted(data['page'], data['limit']))), 200
