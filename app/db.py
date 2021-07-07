from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


# Force mysql to compile fraction of seconds
@compiles(DateTime, "mysql")
def compile_datetime_mysql(type_, compiler, **kw):
    return "DATETIME(6)"


db = SQLAlchemy()


def init_db():
    db.create_all()


def clear_db():
    db.drop_all()
