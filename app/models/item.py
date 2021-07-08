from sqlalchemy import desc

from app.db import db
from .base import BaseModel


class ItemModel(BaseModel):
    __tablename__ = 'item'

    name: str = db.Column(db.String(20), unique=True)
    description: str = db.Column(db.String(200))
    price: float = db.Column(db.Numeric(10, 2))
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

    @classmethod
    def get_items_by_category_id(cls, category_id, page, limit):
        offset = (page - 1) * limit
        return cls.query.filter_by(category_id=category_id).offset(offset).limit(limit).all()

    @classmethod
    def get_latest_items(cls, page, limit):
        offset = (page - 1) * limit
        return cls.query.order_by(desc(cls.updated_time)).offset(offset).limit(limit).all()

    @classmethod
    def get_item_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_total_items_number(cls):
        return cls.query.count()

    @classmethod
    def get_category_items_number(cls, category_id):
        return cls.query.filter_by(category_id=category_id).count()
