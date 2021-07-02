from flask import Blueprint, jsonify

from app.models.item import ItemModel

item_blueprint = Blueprint('item_blueprint', __name__, url_prefix='/categories/<category_id>/items')


@item_blueprint.route('', methods=['POST'])
def create_item(category, data, user_id):
    new_item = ItemModel(**data, category_id=category.id, user_id=user_id)
    new_item.save()
    return


@item_blueprint.route('/<item_id>', methods=['GET'])
def get_item_by_id(item, item_id, category_id):
    pass


@item_blueprint.route('', methods=['GET'])
def get_items_by_category_id(category, data):
    total = category.id
    offset = (data['page'] - 1) * data['offset']
    items = ItemModel.query \
        .filter_by(category_id=category.id) \
        .offset(data['offset']) \
        .limit(data['limit']) \
        .all()
    return jsonify(items)
