from flask import Blueprint, jsonify

from app.models.category import CategoryModel

category_blueprint = Blueprint('category_blueprint', __name__, url_prefix='/categories')


@category_blueprint.route('', methods=['GET'])
def get_categories():
    categories = CategoryModel.get_all_category()
    return jsonify(categories), 200
