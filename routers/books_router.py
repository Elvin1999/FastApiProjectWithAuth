from fastapi import FastAPI, HTTPException, Query, Depends, APIRouter
from typing import Optional,List
from sqlalchemy.orm import Session

from deps import get_db
from helpers import paginate
from models import Author, Book
from schemas import BookOut, BookCreate

router=APIRouter(prefix="/api/books",tags=["books"])

@router.post('/',response_model=BookOut,status_code=201)
def create_book(payload:BookCreate,db:Session=Depends(get_db)):
    if not db.query(Author).get(payload.author_id):
        raise HTTPException(status_code=404,detail='Author not found')
    book=Book(title=payload.title,pages=payload.pages,author_id=payload.author_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return BookOut.from_orm(book)

@router.get('/',response_model=dict,status_code=200)
def list_books(
        q:Optional[str]=Query(None),
        author_id:Optional[int]=Query(None),
        order:str=Query("-id"),
        page:int=Query(1,ge=1),
        size:int=Query(10,ge=1,le=100),
        db:Session=Depends(get_db)):
    query=db.query(Book)
    if author_id:
        query=query.filter(Book.author_id==author_id)
    if q:
        query=query.filter(Book.title.icontains(q.lower()))
    if order.lstrip('-') not in {"title","id","pages"}:
        order="-id"
    col=getattr(Book,order.lstrip('-'))
    if order.startswith('-'): col=col.desc()
    query=query.order_by(col)
    data=paginate(query,page=page,size=size)
    data["results"]=[BookOut.from_orm(b) for b in data["results"]]
    return data

@router.patch('/{book_id}',response_model=BookOut,status_code=200)
def update_book(book_id:int,payload:BookCreate,db:Session=Depends(get_db)):
    b=db.query(Book).get(book_id)
    if b is None:
        raise HTTPException(status_code=404,detail='Book not found')
    if payload.author_id and not db.query(Author).get(payload.author_id):
        raise HTTPException(status_code=404,detail='Author not found')

    b.title=payload.title
    b.pages=payload.pages
    b.author_id=payload.author_id
    db.commit()
    db.refresh(b)
    return BookOut.from_orm(b)