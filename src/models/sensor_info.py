# from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
# from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship
# from src.db.database import Base


# class SensorInfo(Base):
#     __tablename__ = "sensor_info"

#     id = Column(Integer, primary_key=True, index=True)
#     label = Column(String(100), nullable=False)
#     location = Column(String(255))
#     gateway_id = Column(Integer, ForeignKey("gateway.id", ondelete="CASCADE"))
#     no_of_devices = Column(Integer)
#     hardware_model = Column(String(100))
#     device_no = Column(String(100))
#     sensor_type = Column(String(50), nullable=False)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

#     gateway = relationship("Gateway", back_populates="sendo_info")
#     readings = relationship("SensorReading", back_populates="sensor", cascade="all, delete")