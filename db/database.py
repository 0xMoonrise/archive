import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

LOCAL="postgresql://postgresql:postgresql@127.0.0.1:5432/archive"
DATABASE_URL = os.environ.get('DB_URI', LOCAL)

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

