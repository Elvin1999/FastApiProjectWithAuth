from sqlalchemy.orm import Session
from database import Base
from models import User

def test_register_login_me(client,db_session:Session):
    #Register
    r=client.post("/api/auth/register",json={
        "email":"normal@gmail.com",
        "password":"normal123",
        "role":"user"
    })

    assert r.status_code in (200,201),r.text
    data=r.json()
    assert data['email']=="normal@gmail.com"
    assert data['role']=="user"

    #Login

    r2=client.post("/api/auth/login",json={"email":"normal@gmail.com","password":"normal123"})

    assert r2.status_code == 200,r2.text
    token=r2.json()["access_token"]
    assert token

    #me

    r3=client.get("/api/auth/me",headers={"Authorization":f"Bearer {token}"})
    assert r3.status_code == 200
    me=r3.json()
    assert me["email"]=="normal@gmail.com"
    assert me["role"]=="user"

def test_login_wrong_password(client,db_session:Session,normal_user):
    r=client.post("/api/auth/login",json={
        "email":"normal@gmail.com",
        "password":"WRONGPASS",
    })
    assert r.status_code == 401,r.text

def test_register_duplicate_email(client,db_session,normal_user):
    r=client.post("/api/auth/register",json={
        "email":"normal@gmail.com",
        "password":"Another password",
        "role":"user"
    })
    assert r.status_code in (400,409)
