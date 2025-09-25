from fastapi import FastAPI
from database import Base,engine
from routers import auth_router,books_router,authors_router

Base.metadata.create_all(bind=engine)

app=FastAPI(title='FastAPI with JWT and Roles')
app.include_router(auth_router)
app.include_router(books_router)
app.include_router(authors_router)