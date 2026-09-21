import pytest

from app import create_app
from app.db import db as _db


@pytest.fixture(scope='session')
def app():
    """Create the application using the testing config."""
    app = create_app('testing')

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    """Test client with a fresh request context per test."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI test runner."""
    return app.test_cli_runner()