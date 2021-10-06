"""
Module initializes Flask app and registers blueprints defined in routes module.
"""

# Third-part
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_mail import Mail

_DB = SQLAlchemy()
_STATIC_FOLDER: str = ""
_BCRYPT = None
_LOGIN_MANAGER = None
_MARSH = Marshmallow()
_MAIL = None


def create_app():
    global _DB, _STATIC_FOLDER, _BCRYPT, _LOGIN_MANAGER, _MARSH, _MAIL

    app = Flask(__name__)
    app.config.from_object("config.Config")

    _DB = SQLAlchemy(app)
    _MARSH = Marshmallow(app)

    _STATIC_FOLDER = app.static_folder
    _BCRYPT = Bcrypt(app)
    _LOGIN_MANAGER = LoginManager(app)
    _LOGIN_MANAGER.login_view = "server.login"
    _LOGIN_MANAGER.login_message_category = "info"
    _MAIL = Mail(app)

    # Blueprints
    from blood_analyzer.server import SERVER_BLUEPRINTS
    app.register_blueprint(SERVER_BLUEPRINTS)

    _DB.create_all()
    return app
