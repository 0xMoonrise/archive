from sqlalchemy.orm import Session
from models import Archive

def get_by_id(db, id):
    return db.query(Archive).filter(Archive.id == id).first()

def get_all_images(db):
    return db.query(Archive.thumbnail_image,
                    Archive.filename).filter(Archive.filename.like("%pdf")).all()
    
def get_filenames(db, offset=0, limit=8):
    return [filename for (filename,) in db.query(Archive.filename)
                                          .offset(offset)
                                          .limit(limit)
                                          .all()]

def count_files(db):
    return db.query(Archive).count()

def get_by_name(db, name, offset=0, limit=8):
    return [filename for (filename,) in db.query(Archive.filename)
                                          .filter(Archive.filename
                                                         .like(f"%{name}%"))
                                          .offset(offset)
                                          .limit(limit)
                                          .all()]

def count_by_name(db, name):
    return db.query(Archive).filter(Archive.filename
                                           .like(f"%{name}%")).count()

def get_file_by_name(db, name):
    return db.query(Archive).filter(Archive.filename == name).first()

def get_thumbnail_by_name(db, name):
    name = name.rsplit('.', 1)[0] #Without extension
    return db.query(Archive.thumbnail_image).filter(Archive.filename.like(f"{name}%")).scalar()
#thumbnail_image
