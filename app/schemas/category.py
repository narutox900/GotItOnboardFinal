from marshmallow import Schema, fields, validate


class CreateCategorySchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=20), required=True)
    description = fields.Str(validate=validate.Length(min=1, max=100), required=True)


class GetCategorySchema(CreateCategorySchema):
    id = fields.Integer()
