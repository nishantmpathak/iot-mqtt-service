# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from src.db.database import Base


# class UserAuth(Base):
#     __tablename__ = "user_auth"

#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
#     user_name = Column(String(100), unique=True, nullable=False)
#     password = Column(String(255), nullable=False)

#     user = relationship("Users", back_populates="auth")