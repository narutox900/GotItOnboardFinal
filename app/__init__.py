import os

from flask import Flask, jsonify

from app.controllers.item import item_blueprint
from app.controllers.category import category_blueprint
from app.models import category, item, user


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object('app.config.config.DevConfig')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.register_blueprint(item_blueprint)
    app.register_blueprint(category_blueprint)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from app.db import db
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app
