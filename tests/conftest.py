import os
import sys
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api import router_auth, router_blog, router_project, router_tag, router_user
from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.models import User
from app.utils.hashing import hash_password


def start_application() -> FastAPI:
    app = FastAPI()
    app.include_router(router_auth, prefix="/api")
    app.include_router(router_blog, prefix="/api")
    app.include_router(router_project, prefix="/api")
    app.include_router(router_tag, prefix="/api")
    app.include_router(router_user, prefix="/api")
    return app


DB_URL = settings.TEST_DB_URL
engine = create_engine(DB_URL)
session_testing = sessionmaker(autocommit=False, autoflush=True, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a new FastAPI app for testing.
    """

    Base.metadata.create_all(bind=engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[Session, Any, None]:
    """
    Create a new database session for testing.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = session_testing(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    """
    Create a TestClient for the FastAPI app.
    """

    def get_test_db() -> Generator[Session, Any, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def test_user(db_session: Session) -> User:
    user_data = {
        "username": "testuser",
        "email": "test@gmail.com",
        "password": hash_password("SecurePassword123"),
        "is_active": True,
    }

    from app.crud import crud_create_user

    user = crud_create_user(user_data, db=db_session)
    return user
