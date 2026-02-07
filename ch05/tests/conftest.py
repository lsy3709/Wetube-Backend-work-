# pytest 픽스처 – Flask 앱·클라이언트·DB
import os

import pytest

from app import create_app, db


@pytest.fixture
def app():
    """테스트용 Flask 앱. DB는 in-memory SQLite로 격리."""
    prev = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    try:
        app = create_app()
        app.config["TESTING"] = True
        yield app
    finally:
        if prev is not None:
            os.environ["DATABASE_URL"] = prev
        elif "DATABASE_URL" in os.environ:
            del os.environ["DATABASE_URL"]


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def app_ctx(app):
    """앱 컨텍스트 (모델/DB 테스트용)."""
    with app.app_context():
        yield app


@pytest.fixture
def real_app():
    """실제 DB 사용 (instance/wetube.db) – 시드 데이터 삽입용."""
    app = create_app()
    app.config["TESTING"] = True
    return app
