# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from src.db.database import Base


# class Role(Base):
#     __tablename__ = "role"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
#     sensor_type_access = Column(String(50))
#     gateway_id = Column(Integer, ForeignKey("gateway.id", ondelete="CASCADE"))

#     user = relationship("Users", back_populates="roles")
#     gateway = relationship("Gateway", back_populates="roles")