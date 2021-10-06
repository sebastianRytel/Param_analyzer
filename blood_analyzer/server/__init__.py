"""
Module is used for creating blueprints, further used in routes.
"""

from flask import Blueprint

SERVER_BLUEPRINTS = Blueprint("server", __name__)

from . import routes
