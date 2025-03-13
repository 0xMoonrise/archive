from sqlalchemy import text
from .database import SessionLocal, engine
from .base import Base
from .archive import Archive

with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS archive_schema"))
    conn.commit()

Base.metadata.create_all(engine)
