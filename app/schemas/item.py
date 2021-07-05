from marshmallow import Schema, fields, validate


class CreateItemSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=20), required=True)
    description = fields.Str(validate=validate.Length(min=1, max=100), required=True)
    price = fields.Float(validate=validate.Range(min=0, min_inclusive=False), required=True)


class GetItemSchema(CreateItemSchema):
    id = fields.Integer()
    category_id = fields.Integer()
    user_id = fields.Integer()
