from flask import Blueprint

bp = Blueprint('health', __name__)

from app.modules.health import routes