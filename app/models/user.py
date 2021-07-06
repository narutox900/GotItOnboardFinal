import re

from werkzeug.security import generate_password_hash

from app.db import db
from .base import BaseModel
from app.utils.exception import BadRequestException
from app.utils.messages.message import INVALID_PASSWORD


class UserModel(BaseModel):
    __tablename__ = 'user'
    username: str = db.Column(db.String(20), unique=True)
    password: str = db.Column(db.String(200))
    items = db.relationship('ItemModel', backref='item_author', lazy='joined')
    categories = db.relationship('CategoryModel', backref='category_author', lazy='joined')

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
