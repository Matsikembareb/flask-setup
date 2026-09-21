"""Error handlers blueprint — registers app-wide HTTP and database error responses."""
from flask import Blueprint

bp = Blueprint('errors', 'errors')

from app.modules.errors import errors

__all__ = ['bp']

