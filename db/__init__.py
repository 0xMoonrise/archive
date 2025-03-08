from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URL = "postgresql://postgresql:postgresql@127.0.0.1:5432/archive"

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_pdfs(pdf_id=None, filename=None, editorial=None, favorite=False):
    """Obtiene PDFs con filtros opcionales."""
    session = SessionLocal()
    try:
        query = session.query(PDFFile)

        if pdf_id:
            query = query.filter(PDFFile.id == pdf_id)
        if filename:
            query = query.filter(PDFFile.filename.ilike(f"%{filename}%"))
        if editorial:
            query = query.filter(PDFFile.editorial.ilike(f"%{editorial}%"))
        if favorite is not None:
            query = query.filter(PDFFile.favorite == favorite)

        return query.all()
    finally:
        session.close()
