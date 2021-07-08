import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from app.controllers.category import category_blueprint
from app.controllers.item import category_item_blueprint, all_item_blueprint
from app.controllers.user import register_blueprint, login_blueprint
from app.db import db, init_app
from app.models import category, item, user
from app.utils.exception import CustomException


def create_app():
    # create and configure the app
    app = Flask(__name__)

    env = os.getenv('FLASK_ENV').capitalize()
    app.config.from_object(f'app.config.config.{env}Config')

    app.register_blueprint(category_item_blueprint)
    app.register_blueprint(all_item_blueprint)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(register_blueprint)
    app.register_blueprint(login_blueprint)

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify(message=e.description), e.code

    @app.errorhandler(CustomException)
    def handle_custom_exception(e):
        return jsonify(e.body), e.status_code

    db.init_app(app)
    init_app(app)

    return app
