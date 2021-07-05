from marshmallow import Schema, fields, validate


class PaginationSchema(Schema):
    limit = fields.Integer(validate=validate.Range(min=1, max=50), missing=10)
    page = fields.Integer(validate=validate.Range(min=1), missing=1)
