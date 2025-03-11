from sqlalchemy import Column, Integer, String, Boolean, DateTime, LargeBinary, event
from datetime import datetime
from .database import Base

class PDFFile(Base):
    __tablename__ = "pdf_files"
    __table_args__ = {'schema': 'pdf_schema'}

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    editorial = Column(String, nullable=False)
    cover_page = Column(Integer, default=1, nullable=False)
    data = Column(LargeBinary, nullable=False)
    favorite = Column(Boolean, default=False, nullable=False)
    thumbnail_image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<PDFFile(id={self.id}, filename={self.filename})>"

