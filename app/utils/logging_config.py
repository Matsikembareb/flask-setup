"""Logging configuration — rotating file handler + optional SMTP error emails."""
import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import Flask


def setup_error_logging(app: Flask) -> None:
    """Configure application logging.

    Always enabled
    --------------
    Rotating file handler writing to ``app.log`` at the project root.
    Captures INFO and above, rotates at 10 MB, keeps 10 backups.

    Conditionally enabled (requires .env / environment variables)
    --------------------------------------------------------------
    SMTP handler that emails ERROR-level events to ``ADMINS``.
    Requires: MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, ADMINS.
    """
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # --- File handler (disabled during testing) ------------------------------
    # Skip file I/O in tests — pytest should leave the filesystem clean.
    if not app.config.get('TESTING'):
        log_dir = os.path.dirname(os.path.abspath(__file__))
        log_file = os.path.normpath(
            os.path.join(log_dir, '..', '..', 'app.log')
        )
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10_485_760,  # 10 MB
            backupCount=10,
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

    # --- Email handler (optional) -------------------------------------------
    if app.config.get('ADMINS') and app.config.get('MAIL_SERVER'):
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=app.config['MAIL_FROM'],
            toaddrs=app.config['ADMINS'],
            subject=f"Application Error [{os.environ.get('APP_ENV', 'development')}]",
            credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),
            secure=() if app.config['MAIL_USE_TLS'] else None,
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(formatter)
        app.logger.addHandler(mail_handler)

    app.logger.setLevel(logging.INFO)

