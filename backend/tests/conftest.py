# backend/tests/conftest.py
import pytest
import sys
from pathlib import Path

# Ensure backend folder is on sys.path
BACKEND_DIR = Path(__file__).resolve().parents[1]  # .../backend
sys.path.insert(0, str(BACKEND_DIR))

from app import create_app
from extensions import db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()

    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",  # in-memory DB
        JWT_SECRET_KEY="test-secret-key",
    )

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Flask test client (simulate HTTP requests)."""
    return app.test_client()
