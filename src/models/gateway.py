from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.db.database import Base


class Gateway(Base):
    __tablename__ = "gateway"

    id = Column(Integer, primary_key=True, index=True)
    imei = Column(String(50), unique=True, nullable=False)
    location = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())

    devices = relationship("DeviceInfo", back_populates="gateway")



class DeviceInfo(Base):
    __tablename__ = "device_info"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(100), nullable=False)
    location = Column(String(255))
    gateway_id = Column(Integer, ForeignKey("gateway.id", ondelete="CASCADE"))
    no_of_devices = Column(Integer)
    hardware_model = Column(String(100))
    device_no = Column(String(100))
    device_type = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    gateway = relationship("Gateway", back_populates="devices")
    # readings = relationship("SensorReading", back_populates="sensor", cascade="all, delete")