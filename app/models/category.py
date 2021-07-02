from app.db import db
from .base import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = 'category'

    name: str = db.Column(db.String(20))
    description: str = db.Column(db.String(200))
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('ItemModel', lazy='dynamic')

    def update(self, name, description):
        self.name = name
        self.description = description
        db.session.commit()

    @classmethod
    def get_category_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all_category(cls):
        return {'categories': [category.json() for category in cls.query.all()]}
