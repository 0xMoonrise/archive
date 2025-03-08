from sqlalchemy.orm import Session
from .models import PDFFile

def get_pdf_by_id(db, pdf_id):
    return db.query(PDFFile).filter(PDFFile.id == pdf_id).first()

def get_pdfs(db, skip=0, limit=100):
    return db.query(PDFFile).offset(skip).limit(limit).all()

