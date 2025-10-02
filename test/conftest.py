import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base
from deps import get_db
from models import User,Role
from auth import hash_password


TEST_ENGINE=create_engine('sqlite://',
                          connect_args={'check_same_thread': False},
                          poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=TEST_ENGINE)

Base.metadata.create_all(bind=TEST_ENGINE)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)

def create_user(db,email:str,password:str,role:Role=Role.user,active:bool=True):
    u=User(
        email=email.lower(),
        password_hash=hash_password(password),
        role=role,
        is_active=active
    )

    db.add(u)
    db.commit()
    db.refresh(u)
    return u

@pytest.fixture
def db_session():
    session=TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def admin_user(db_session):
    return create_user(db_session,"admin@gmail.com","admin123",role=Role.admin)

@pytest.fixture
def normal_user(db_session):
    return create_user(db_session,"normal@gmail.com","normal123",role=Role.user)

def login_and_get_token(client:TestClient,email:str,password:str)-> str:
    resp=client.post("/api/auth/login",json={"email":email,"password":password})
    assert resp.status_code==200,resp.text
    return resp.json()["access_token"]