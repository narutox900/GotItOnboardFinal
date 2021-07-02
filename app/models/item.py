from decimal import Decimal

from app.db import db
from .base import BaseModel


class ItemModel(BaseModel):
    __tablename__ = 'item'

    name: str = db.Column(db.String(20))
    description: str = db.Column(db.String(200))
    price: Decimal = db.Column(db.Numeric(10, 2))
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id: int = db.Column(db.Integer, db.ForeignKey('category.id'))

    def update(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price
        db.session.commit()

    @classmethod
    def get_item_by_id(cls, item_id, category_id):
        return cls.query.filter_by(id=item_id, category_id=category_id).first()
