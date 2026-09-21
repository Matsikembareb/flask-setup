"""Global HTTP and database error handlers.

All responses follow the same JSON shape::

    {"error": "<short title>", "message": "<human-readable detail>"}
"""
from flask import jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.db import db
from app.modules.errors import bp


@bp.app_errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': str(error)}), 400


@bp.app_errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication is required.'}), 401


@bp.app_errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to access this resource.'}), 403


@bp.app_errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found.'}), 404


@bp.app_errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method Not Allowed', 'message': str(error)}), 405


@bp.app_errorhandler(422)
def unprocessable_entity(error):
    return jsonify({'error': 'Unprocessable Entity', 'message': str(error)}), 422


# IntegrityError must be registered BEFORE SQLAlchemyError.
# IntegrityError is a subclass of SQLAlchemyError — Flask resolves
# handlers by MRO (most specific first), so order matters here.
@bp.app_errorhandler(IntegrityError)
def handle_integrity_error(error):
    db.session.rollback()
    return jsonify({
        'error': 'Conflict',
        'message': 'A database constraint was violated. This resource may already exist.',
    }), 409


@bp.app_errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(error):
    db.session.rollback()
    return jsonify({
        'error': 'Database Error',
        'message': 'An unexpected database error occurred.',
    }), 500


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred. Please try again later.',
    }), 500

