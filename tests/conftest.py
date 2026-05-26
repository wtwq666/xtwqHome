"""Test env: isolated SQLite DB and upload directory."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

BACKEND_ROOT = Path(__file__).resolve().parent.parent
TEST_DATA_DIR = BACKEND_ROOT / ".pytest_cache" / "data"
TEST_UPLOAD_DIR = BACKEND_ROOT / ".pytest_cache" / "uploads"

os.environ["DATABASE_URL"] = f"sqlite:///{(TEST_DATA_DIR / 'test.db').as_posix()}"
os.environ["UPLOAD_DIR"] = str(TEST_UPLOAD_DIR)
os.environ["STORAGE_BACKEND"] = "local"
os.environ["PG_HOST"] = ""

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.storage import reset_storage  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_db() -> None:
    TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if TEST_UPLOAD_DIR.exists():
        shutil.rmtree(TEST_UPLOAD_DIR)
    TEST_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    reset_storage()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    reset_storage()


@pytest.fixture
def db() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
