from flask import Blueprint, jsonify
from werkzeug.security import check_password_hash

from app.models.user import UserModel
from app.schemas.user import CreateUserSchema, GetUserSchema
from app.utils.exception import AuthenticationException
from app.utils.messages.message import INVALID_CREDENTIALS
from app.utils.security import encode_token
from app.utils.validation import load_and_validate_data, duplicate_username_validate, logged_in_validate

register_blueprint = Blueprint('register_blueprint', __name__, url_prefix='/register')
login_blueprint = Blueprint('login_blueprint', __name__, url_prefix='/login')


@register_blueprint.route('', methods=['POST'])
@load_and_validate_data(CreateUserSchema)
@logged_in_validate
@duplicate_username_validate
def register(data):
    user = UserModel(**data)
    user.save()
    return jsonify(message='Registered successfully'), 200


@login_blueprint.route('', methods=['POST'])
@logged_in_validate
@load_and_validate_data(GetUserSchema)
def login(data):
    user = UserModel.get_user_by_username(data['username'])
    if user and check_password_hash(user.password, data['password']):
        token = encode_token({'uid': user.id})
        return jsonify(access_token=token, uid=user.id), 200

    raise AuthenticationException(INVALID_CREDENTIALS)
