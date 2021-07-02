from marshmallow import Schema, fields, validate


class CreateUserSchema(Schema):
    username = fields.Str(validate=validate.Length(min=1, max=20), required=True)
    password = fields.Str(validate=validate.Length(min=1, max=20), required=True)
