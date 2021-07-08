import click

from flask.cli import with_appcontext
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


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


@click.command("clear-db")
@with_appcontext
def clear_db_command():
    clear_db()
    click.echo("Cleared the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.cli.add_command(init_db_command)
    app.cli.add_command(clear_db_command)
