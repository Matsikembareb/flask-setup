"""Health check and API discovery module."""
from flask import Blueprint

bp = Blueprint('health', __name__)

from app.modules.health import routes  # noqa: F401

__all__ = ['bp']