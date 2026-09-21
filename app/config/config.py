import os
from pathlib import Path

from dotenv import load_dotenv


# Load variables from the project root .env (next to run.py).
# Falls back to the repo parent so monorepos work too.
_project_root = Path(__file__).resolve().parents[2]
_repo_root = _project_root.parent
_project_env = _project_root / '.env'
_repo_env = _repo_root / '.env'

if _project_env.exists():
    load_dotenv(_project_env)
else:
    load_dotenv(_repo_env)


class BaseConfig:
    """Base configuration shared by all environments."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

    # OpenAPI / Swagger (flask-smorest)
    API_TITLE = 'Flask API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-key-change-in-production')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRY_HOURS = 1

    # Email error logging (optional — configure via .env)
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM', 'noreply@yourapp.com')
    ADMINS = os.getenv('ADMINS', '').split(',') if os.getenv('ADMINS') else []

    # CORS — comma-separated origins in .env, e.g. http://localhost:3000,https://yourapp.com
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///development.db')


class TestingConfig(BaseConfig):
    """Testing configuration — always uses an in-memory SQLite database.

    DATABASE_URL is intentionally ignored here: if the .env sets it to a
    real file (e.g. sqlite:///development.db), tests would silently mutate
    the development database.
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # validated in create_app


def get_config_by_name(config=None):
    """Return the config object matching the given environment name.

    Parameters
    ----------
    config : str or None
        ``'development'``, ``'testing'``, or ``'production'``.
        When ``None`` (default) the value is read from ``APP_ENV``
        at call time — not at import time — avoiding stale defaults.
        Falls back to ``DevelopmentConfig`` when the value is unrecognised.
    """
    if config is None:
        config = os.environ.get('APP_ENV', 'development')
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }
    return configs.get(config, DevelopmentConfig)()
