from marshmallow import Schema, fields, validate

from app.schemas.category import GetCategorySchema
from app.schemas.item import GetItemSchema


class PaginationSchema(Schema):
    limit = fields.Integer(validate=validate.Range(min=1, max=50), missing=10)
    page = fields.Integer(validate=validate.Range(min=1), missing=1)


class GetPaginationSchema(Schema):
    total = fields.Integer()
    limit = fields.Integer()


class CategoryPaginationSchema(GetPaginationSchema):
    categories = fields.List(fields.Nested(GetCategorySchema))


class ItemPaginationSchema(GetPaginationSchema):
    items = fields.List(fields.Nested(GetItemSchema))
