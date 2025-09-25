from fastapi import FastAPI,HTTPException,Query,Depends
from typing import Optional,List
from pydantic import BaseModel,Field
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func, Enum as SAEnum, Boolean
from sqlalchemy.orm import declarative_base,relationship,sessionmaker,Session
from enum import Enum
from database import Base

# SqlAlchemy Models
class Author(Base):
    __tablename__ = 'authors'
    id=Column(Integer,primary_key=True)
    name=Column(String(120),nullable=False)
    books=relationship('Book',back_populates='author',cascade='all, delete-orphan')

class Book(Base):
    __tablename__ = 'books'
    id=Column(Integer,primary_key=True)
    title=Column(String(120),nullable=False)
    pages=Column(Integer,nullable=False,default=1)
    author_id=Column(Integer,ForeignKey('authors.id'),nullable=False)
    author=relationship('Author',back_populates='books')

class Role(str,Enum):
    admin='admin'
    user='user'

class User(Base):
    __tablename__ = 'users'
    id=Column(Integer,primary_key=True)
    email=Column(String(255),unique=True,nullable=False,index=True)
    password_hash=Column(String(255),nullable=False)
    role=Column(SAEnum(Role),nullable=False,default=Role.user)
    is_active=Column(Boolean,nullable=False,default=True)