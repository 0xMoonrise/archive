from sqlalchemy import (
    Column, 
    Integer,
    String,
    Boolean,
    DateTime,
    LargeBinary,
    CheckConstraint,
    func
)
from datetime import datetime
from .base import Base

class Archive(Base):
    __tablename__ = "archive"
    __table_args__ = (
        CheckConstraint("cover_page >= 1", name="check_cover_page_positive"),
        {"schema": "archive_schema"}
    )

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    editorial = Column(String, nullable=False)
    cover_page = Column(Integer, server_default="1", nullable=False)
    file = Column(LargeBinary, nullable=False)
    favorite = Column(Boolean, server_default="false", nullable=False)
    thumbnail_image = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Archive(id={self.id}, filename={self.filename})>"
