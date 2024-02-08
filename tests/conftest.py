import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dependencies.database import get_db
from main import app
from models.contacts import Base, User
from services.auth import auth_service, Auth

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@pytest.fixture(scope="module")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def session_with_existing_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    existing_user = User(email="test_user@test.com", password=Auth().get_password_hash("test_password"))
    db.add(existing_user)
    db.commit()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope="module")
def user():
    return {"email": "test_user@test.com", "password": Auth().get_password_hash("test_password"),
            "access_token": "test_access_token", "refresh_token": "test_refresh_token"}


@pytest.fixture(scope="module")
def client_with_user(session):
    client = TestClient(app)
    db = session
    user = User(
        email="test_user@test.com",
        password="test_password",
    )

    user.password = Auth().get_password_hash(user.password)
    user.refresh_token = "refresh_token"
    user.access_token = "access_token"
    db.add(user)
    db.commit()
    yield client, user
    db.delete(user)
    db.commit()
    db.close()
