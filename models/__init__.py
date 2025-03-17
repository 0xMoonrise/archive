from sqlalchemy import text, inspect
from .database import SessionLocal, engine
from .base import Base
from .archive import Archive

with engine.connect() as conn:
    try:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS archive_schema"))
        conn.commit()
    except IntegrityError:
        conn.rollback()
    finally:
        conn.close()

inspector = inspect(engine)
if "archive" not in inspector.get_table_names():
    Base.metadata.create_all(engine)
