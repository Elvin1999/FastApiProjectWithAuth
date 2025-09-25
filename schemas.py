
from typing import Optional,List
from pydantic import BaseModel, Field, EmailStr
from models import Role

# Pydantic Schemas
class BookCreate(BaseModel):
    title:str=Field(min_length=1,max_length=128)
    pages:int=Field(ge=1)
    author_id:int

class BookOut(BaseModel):
    id:int
    title:str
    pages:int
    author_id:int
    class Config:from_attributes=True

class AuthorCreate(BaseModel):
    name:str=Field(min_length=1,max_length=120)

class AuthorOut(BaseModel):
    id:int
    name:str
    books:List[BookOut]
    class Config:from_attributes=True

class UserRegister(BaseModel):
    email:EmailStr
    password:str=Field(min_length=6,max_length=128)
    role: Optional[Role]=Role.user

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    role:Role
    is_active:bool
    class Config:
        from_attributes=True

class TokenOut(BaseModel):
    access_token:str
    token_type:str='Bearer'
