import datetime

from app.db import db


class BaseModel(db.Model):
    __abstract__ = True

    id: int = db.Column(db.Integer, primary_key=True)
    created_time: datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_time: datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()