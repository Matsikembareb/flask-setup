"""WSGI entry point — used by gunicorn in production.

Usage:
    gunicorn wsgi:app
    gunicorn --bind 0.0.0.0:5000 wsgi:app
"""
from app import create_app

app = create_app()

