from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import PDFFile

def get_by_id(db, pdf_id):
    return db.query(PDFFile).filter(PDFFile.id == pdf_id).first()

def get_all_images(db):
    return db.query(PDFFile.thumbnail_image,
                    PDFFile.filename).filter(PDFFile.filename.like("%pdf")).all()
    
def get_filenames(db, offset=0, limit=8):
    return [filename for (filename,) in db.query(PDFFile.filename)
                                          .offset(offset)
                                          .limit(limit)
                                          .all()]

def count_files(db):
    return db.query(PDFFile).count()

def get_by_name(db, name, offset=0, limit=8):
    return [filename for (filename,) in db.query(PDFFile.filename)
                                          .filter(PDFFile.filename
                                                         .like(f"%{name}%"))
                                          .offset(offset)
                                          .limit(limit)
                                          .all()]

def count_by_name(db, name):
    return db.query(PDFFile).filter(PDFFile.filename
                                           .like(f"%{name}%")).count()

def get_file_by_name(db, name):
    return db.query(PDFFile).filter(PDFFile.filename == name).first()

def get_thumbnail_by_name(db, name):
    name = name.rsplit('.', 1)[0] #Without extension
    return db.query(PDFFile).filter(PDFFile.filename.like(f"{name}%")).first()
#thumbnail_image
