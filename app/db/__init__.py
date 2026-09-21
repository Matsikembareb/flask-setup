"""Database instance — import `db` from here throughout the app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

__all__ = ['db']

