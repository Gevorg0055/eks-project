from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
