# from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship
# from src.db.database import Base


# class Users(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False)
#     organization = Column(String(150))
#     email = Column(String(150), unique=True)
#     phone_no = Column(String(20))
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

#     roles = relationship("Role", back_populates="user", cascade="all, delete")
#     auth = relationship("UserAuth", back_populates="user", uselist=False)