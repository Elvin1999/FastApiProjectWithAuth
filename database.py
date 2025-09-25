from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,relationship,sessionmaker,Session

DATABASE_URL = 'sqlite:///./fastapi_books.db'
engine = create_engine(DATABASE_URL,connect_args={'check_same_thread':False})
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()
