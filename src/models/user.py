from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    hashed_password = Column(String, nullable=False)
    checks = relationship("Check", back_populates="user")