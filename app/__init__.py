import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from app.controllers.item import item_blueprint, all_item_blueprint
from app.controllers.category import category_blueprint
from app.controllers.user import register_blueprint, login_blueprint
from app.models import category, item, user
from app.utils.exception import CustomException


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        # load the test config if passed in
        app.config.from_object('app.config.config.TestConfig')
    else:
        # load the instance config, if it exists, when not testing
        app.config.from_object('app.config.config.DevConfig')

    app.register_blueprint(item_blueprint)
    app.register_blueprint(all_item_blueprint)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(register_blueprint)
    app.register_blueprint(login_blueprint)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify(message=e.description), e.code

    @app.errorhandler(CustomException)
    def handle_custom_exception(e):
        return jsonify(e.body), e.status_code

    from app.db import db
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app
