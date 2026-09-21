"""Flask application factory."""
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_smorest import Api

from app.config.config import get_config_by_name
from app.db import db
from app.utils.logging_config import setup_error_logging

migrate = Migrate()
api = Api()


def create_app(env=None) -> Flask:
    """Create and configure the Flask application.

    Parameters
    ----------
    env : str or config object or None
        Controls which configuration is loaded, in order of priority:

        ``run.py`` passes ``env`` from argparse so you can do:
            python run.py production   without touching ``.flaskenv``.
    """
    app = Flask(__name__)

    # Resolve the config:
    #   None          → get_config_by_name() reads FLASK_ENV
    #   string        → get_config_by_name(string) maps to the right class
    #   config object → used directly
    if env is None:
        config = get_config_by_name()
    elif isinstance(env, str):
        config = get_config_by_name(env)
    else:
        config = env

    app.config.from_object(config)

    # Logging — rotating file handler + optional SMTP (skipped when TESTING=True)
    setup_error_logging(app)

    # CORS — allow configured origins for /api/* and /health* routes
    CORS(app, resources={
        r'/api/*':   {'origins': app.config['CORS_ORIGINS']},
        r'/health*': {'origins': app.config['CORS_ORIGINS']},
    })

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Blueprints — imported here (not at module top) to avoid circular imports
    from app.modules.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.modules.health import bp as health_bp
    app.register_blueprint(health_bp, url_prefix='/health')

    # Register your own blueprints below, e.g.:
    # from app.modules.your_module import bp as your_bp
    # api.register_blueprint(your_bp, url_prefix='/api/your_module')

    return app
