from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.db.database import Base
from sqlalchemy.dialects.postgresql import JSONB

class Gateway(Base):
    __tablename__ = "gateway"

    # Removed __name_pos; use positional arguments for types
    id = Column(Integer, primary_key=True, index=True)
    imei = Column(String(50), unique=True, nullable=False)
    location = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())

    # Simplified relationship declaration
    devices = relationship("DeviceInfo", back_populates="gateway")


class DeviceInfo(Base):
    __tablename__ = "device_info"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(100), nullable=False)
    location = Column(String(255))
    
    # FIXED: ForeignKey is now passed correctly as a positional argument
    gateway_id = Column(Integer, ForeignKey("gateway.id", onupdate="CASCADE", ondelete="CASCADE"))
    
    no_of_devices = Column(Integer)
    hardware_model = Column(String(100))
    device_no = Column(String(100))
    device_type = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    gateway = relationship("Gateway", back_populates="devices")
    readings = relationship("Readings", back_populates="device", cascade="all, delete")


class Readings(Base):
    __tablename__ = "device_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("device_info.id", ondelete="CASCADE"))
    
    data = Column(JSONB, nullable=False) 
    timestamp = Column(DateTime, nullable=False)
    quality_flag = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

    device = relationship("DeviceInfo", back_populates="readings")