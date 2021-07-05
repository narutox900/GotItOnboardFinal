from app.db import db
from .base import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = 'category'

    name: str = db.Column(db.String(20), unique=True)
    description: str = db.Column(db.String(200))
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('ItemModel', lazy='select')

    def update(self, name, description):
        self.name = name
        self.description = description
        db.session.commit()

    def json(self):
        return {'id': self.id, 'name': self.name, 'description': self.description}

    @classmethod
    def get_category_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all_category(cls, page, limit):
        offset = (page - 1) * limit
        return cls.query.offset(offset).limit(limit).all()

    @classmethod
    def get_category_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_total_categories_number(cls):
        return cls.query.count()
