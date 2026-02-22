from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.db.database import Base


class RawMqttEvent(Base):
    __tablename__ = "raw_mqtt_event"

    id = Column(Integer, primary_key=True, index=True)
    gateway_id = Column(Integer, ForeignKey("gateway.id", ondelete="SET NULL"))
    topic = Column(String(255), nullable=False)
    payload_text = Column(Text, nullable=False)
    received_at = Column(DateTime, server_default=func.now())

    # gateway = relationship("Gateway", back_populates="raw_events")