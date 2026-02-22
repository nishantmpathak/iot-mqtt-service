# from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
# from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship
# from src.db.database import Base


# class SensorReading(Base):
#     __tablename__ = "sensor_reading"

#     id = Column(Integer, primary_key=True, index=True)
#     sensor_id = Column(Integer, ForeignKey("sensor_info.id", ondelete="CASCADE"))
#     metric_name = Column(String(50), nullable=False)
#     metric_value = Column(Float, nullable=False)
#     unit = Column(String(20))
#     timestamp = Column(DateTime, nullable=False)
#     quality_flag = Column(String(50))
#     created_at = Column(DateTime, server_default=func.now())

#     sensor = relationship("SensorInfo", back_populates="readings")


# # Composite Index
# Index(
#     "idx_sensor_reading_sensor_timestamp",
#     SensorReading.sensor_id,
#     SensorReading.timestamp.desc()
# )