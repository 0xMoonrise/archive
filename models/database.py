import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

LOCAL = "postgresql://postgresql:postgresql@127.0.0.1:5432/archive"
DATABASE_URL = os.environ.get('DB_URI', LOCAL)

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=60,
    pool_recycle=1800,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
