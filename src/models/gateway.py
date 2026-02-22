from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.db.database import Base


class Gateway(Base):
    __tablename__ = "gateway"

    id = Column(Integer, primary_key=True, index=True)
    imei = Column(String(50), unique=True, nullable=False)
    location = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
