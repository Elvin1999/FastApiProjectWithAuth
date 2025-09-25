from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Role,User
from auth import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_db():
    db:Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db))->User:
    cred_exc=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials",headers={"WWW-Authenticate":"Bearer"})
    try:
        payload=decode_token(token)
        email:str=payload.get("sub")
        if not email:
            raise cred_exc
    except JWTError:
        raise cred_exc

    user=db.query(User).filter(User.email==email).first()
    if not user or not user.is_active:
        raise cred_exc
    return user

def require_roles(*roles:Role):
    def _dep(current:User = Depends(get_current_user)) ->User:
        if current.role not in roles:
            raise HTTPException(status_code=403,detail="Forbidden")
        return current
    return _dep