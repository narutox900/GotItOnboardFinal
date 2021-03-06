from flask import Blueprint, jsonify

from app.models.category import CategoryModel
from app.schemas.category import CreateCategorySchema, GetCategorySchema
from app.schemas.pagination import PaginationSchema, CategoryPaginationSchema
from app.utils.loader import load_category_by_id, dump_schema_decorator
from app.utils.security import token_required
from app.utils.validation import load_and_validate_data, category_owner_validate, duplicate_category_name_validate

category_blueprint = Blueprint('category_blueprint', __name__, url_prefix='/categories')


@category_blueprint.route('', methods=['GET'])
@load_and_validate_data(PaginationSchema)
@dump_schema_decorator(CategoryPaginationSchema)
def get_categories(data):
    categories = CategoryModel.get_all_category(data['page'], data['limit'])
    return {'categories': categories,
            'total': CategoryModel.get_total_categories_number(), 'limit': data['limit']}


@category_blueprint.route('', methods=['POST'])
@token_required
@load_and_validate_data(CreateCategorySchema)
@duplicate_category_name_validate
@dump_schema_decorator(GetCategorySchema)
def create_category(user, data):
    category = CategoryModel(**data)
    category.user_id = user.id
    category.save()
    return category


@category_blueprint.route('/<category_id>', methods=['PUT'])
@token_required
@load_and_validate_data(CreateCategorySchema)
@load_category_by_id
@category_owner_validate
@dump_schema_decorator(GetCategorySchema)
def update_category(category, data, user):
    category.update(**data)
    return category


@category_blueprint.route('/<category_id>', methods=['DELETE'])
@token_required
@load_category_by_id
@category_owner_validate
def delete_category(category, *args, **kwargs):
    category.delete()
    return jsonify(message='Deleted'), 200


@category_blueprint.route('/<category_id>', methods=['GET'])
@load_category_by_id
@dump_schema_decorator(GetCategorySchema)
def get_category(category):
    return category
