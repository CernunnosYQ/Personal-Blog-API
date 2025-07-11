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
from app.core.enums import UserRoles
from app.core.jwt import create_access_token
from app.core.password import hash_password
from app.db.base import Base
from app.db.session import get_db
from tests.utils.schemas import UserExtended


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
def test_user(db_session: Session) -> UserExtended:
    user_data = {
        "username": "testuser",
        "email": "test@gmail.com",
        "password": hash_password("SecurePassword123"),
        "role": UserRoles.USER,
        "is_active": True,
    }

    from app.crud import crud_create_user

    user = crud_create_user(user_data, db=db_session).__dict__
    user["unhashed_password"] = "SecurePassword123"
    user["access_token"] = create_access_token(sub=str(user["id"]))
    return UserExtended(**user)


@pytest.fixture(scope="function")
def test_admin(db_session: Session) -> UserExtended:
    user_data = {
        "username": "testadmin",
        "email": "admin@gmail.com",
        "password": hash_password("SecurePassword123"),
        "role": UserRoles.ADMIN,
        "is_active": True,
    }

    from app.crud import crud_create_user

    user = crud_create_user(user_data, db=db_session).__dict__
    user["unhashed_password"] = "SecurePassword123"
    user["access_token"] = create_access_token(sub=str(user["id"]))
    return UserExtended(**user)
