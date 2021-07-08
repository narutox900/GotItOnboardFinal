import re

from marshmallow import Schema, fields, validate, validates

from app.utils.exception import BadRequestException
from app.utils.messages.message import INVALID_PASSWORD


class GetUserSchema(Schema):
    username = fields.Str(validate=validate.Length(min=1, max=20), required=True)
    password = fields.Str(validate=validate.Length(min=1, max=20), required=True)


class CreateUserSchema(GetUserSchema):

    @validates('password')
    def validate_password(self, value):
        if not re.search('^[A-Za-z0-9.*[!@#$%^&_]+$', value):
            raise BadRequestException(INVALID_PASSWORD)
